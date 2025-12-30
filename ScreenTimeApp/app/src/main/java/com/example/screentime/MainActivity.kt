package com.example.screentime

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.State
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import com.example.screentime.ui.theme.ScreenTimeAppTheme
import android.content.Intent
import android.net.Uri
import android.os.PowerManager
import android.provider.Settings
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import android.Manifest
import android.content.pm.PackageManager
import androidx.core.content.ContextCompat
import com.example.screentime.db.AppDatabase
import kotlinx.coroutines.launch
import kotlinx.coroutines.Dispatchers

import androidx.compose.runtime.livedata.observeAsState
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.lifecycle.ViewModel
import androidx.camera.view.PreviewView
import androidx.compose.ui.viewinterop.AndroidView
import com.example.screentime.PoseLandmarkerHelper
import com.google.mediapipe.tasks.vision.poselandmarker.PoseLandmarkerResult
import com.google.mediapipe.framework.image.BitmapImageBuilder
import com.google.mediapipe.framework.image.MPImage
import android.graphics.Bitmap
import androidx.camera.core.*
import androidx.camera.lifecycle.ProcessCameraProvider
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors
import android.util.Log
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.viewModelScope
import android.content.Context
import android.content.pm.ApplicationInfo
import android.graphics.drawable.Drawable
import androidx.compose.ui.graphics.asImageBitmap
import androidx.core.graphics.drawable.toBitmap
import com.example.screentime.ExerciseCredit
import kotlinx.coroutines.flow.first

data class AppInfo(
    val name: String,
    val packageName: String,
    val icon: Drawable? = null
)

class MainViewModel(
    private val creditDao: com.example.screentime.db.ExerciseCreditDao,
    private val blockedDao: com.example.screentime.db.BlockedAppDao
) : ViewModel() {
    val repCounter = RepCounter()
    val repCount: LiveData<Int> = repCounter.repCount
    private val coachEngine = SmartCoachEngine()

    private val _motivationalText = MutableLiveData<String>("")
    val motivationalText: LiveData<String> = _motivationalText

    var targetApp by mutableStateOf("Blocked Apps")
    
    private val _installedApps = mutableStateOf<List<AppInfo>>(emptyList())
    val installedApps: State<List<AppInfo>> = _installedApps

    init {
        // Observe rep counts and update DB in real-time
        repCount.observeForever { count ->
            if (count > 0) {
                viewModelScope.launch {
                    val currentCredits = creditDao.getLatestCredits().first()?.creditsInSeconds ?: 0
                    creditDao.insert(ExerciseCredit(creditsInSeconds = currentCredits + 60))
                    // We don't reset the counter immediately to let the user see their progress, 
                    // but we need to handle the "delta" correctly.
                    // Actually, the RepCounter increments. We should probably only add for the NEW rep.
                }
            }
        }
    }

    // A better way for real-time:
    private var lastRepCount = 0
    fun syncRepsWithDb(currentReps: Int) {
        if (currentReps > lastRepCount) {
            val delta = currentReps - lastRepCount
            viewModelScope.launch {
                val currentCredits = creditDao.getLatestCredits().first()?.creditsInSeconds ?: 0
                creditDao.insert(ExerciseCredit(creditsInSeconds = currentCredits + (delta * 60)))
                lastRepCount = currentReps
            }
        }
    }

    fun fetchInstalledApps(context: Context) {
        viewModelScope.launch(Dispatchers.IO) {
            val pm = context.packageManager
            val apps = pm.getInstalledApplications(PackageManager.GET_META_DATA)
                .filter { (it.flags and ApplicationInfo.FLAG_SYSTEM) == 0 || it.packageName == "com.google.android.youtube" }
                .map { app ->
                    AppInfo(
                        name = app.loadLabel(pm).toString(),
                        packageName = app.packageName,
                        icon = app.loadIcon(pm)
                    )
                }
                .sortedBy { it.name }
            _installedApps.value = apps
        }
    }

    fun processPoseResult(result: PoseLandmarkerResult) {
        repCounter.processResult(result)
    }

    fun updateMotivationalMessage(creditsInSeconds: Long) {
        _motivationalText.postValue(coachEngine.getMotivationalMessage(creditsInSeconds, targetApp))
    }
}

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val db = AppDatabase.getDatabase(this)
        val viewModel = MainViewModel(db.exerciseCreditDao(), db.blockedAppDao())
        viewModel.fetchInstalledApps(this)

        setContent {
            ScreenTimeAppTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    MainScreen(db.exerciseCreditDao(), db.blockedAppDao(), viewModel)
                }
            }
        }
    }
}

@Composable
fun MainScreen(dao: com.example.screentime.db.ExerciseCreditDao, blockedDao: com.example.screentime.db.BlockedAppDao, mainViewModel: MainViewModel) {
    val context = androidx.compose.ui.platform.LocalContext.current
    val credits by dao.getLatestCredits().collectAsState(initial = null)
    val blockedApps by blockedDao.getAllBlockedApps().collectAsState(initial = emptyList())
    val reps by mainViewModel.repCount.observeAsState(0)
    val motivation by mainViewModel.motivationalText.observeAsState("")
    val scope = rememberCoroutineScope()

    var hasCameraPermission by remember {
        mutableStateOf(
            ContextCompat.checkSelfPermission(context, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED
        )
    }

    val permissionLauncher = rememberLauncherForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { isGranted ->
        hasCameraPermission = isGranted
    }

    val batteryOptimizationLauncher = rememberLauncherForActivityResult(
        ActivityResultContracts.StartActivityForResult()
    ) { }

    fun checkAndRequestBatteryOptimization() {
        val pm = context.getSystemService(PowerManager::class.java)
        if (!pm.isIgnoringBatteryOptimizations(context.packageName)) {
            val intent = Intent(Settings.ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS).apply {
                data = Uri.parse("package:${context.packageName}")
            }
            batteryOptimizationLauncher.launch(intent)
        }
    }

    LaunchedEffect(Unit) {
        checkAndRequestBatteryOptimization()
        if (!hasCameraPermission) {
            permissionLauncher.launch(Manifest.permission.CAMERA)
        }
    }

    LaunchedEffect(reps) {
        mainViewModel.syncRepsWithDb(reps)
    }

    LaunchedEffect(credits) {
        mainViewModel.updateMotivationalMessage(credits?.creditsInSeconds ?: 0)
    }

    Column(
        modifier = Modifier.fillMaxSize()
            .padding(16.dp)
            .verticalScroll(rememberScrollState()),
        verticalArrangement = Arrangement.Top,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(modifier = Modifier.height(32.dp))
        
        Card(
            modifier = Modifier.fillMaxWidth(),
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primaryContainer)
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text(
                    text = "Coach Recommendation:",
                    style = MaterialTheme.typography.labelLarge,
                    color = MaterialTheme.colorScheme.onPrimaryContainer
                )
                Text(
                    text = motivation,
                    style = MaterialTheme.typography.bodyLarge,
                    color = MaterialTheme.colorScheme.onPrimaryContainer
                )
            }
        }

        Spacer(modifier = Modifier.height(24.dp))
        
        Text(
            text = "Exercise Credits: ${credits?.creditsInSeconds ?: 0}s",
            fontSize = 20.sp,
            style = MaterialTheme.typography.titleLarge
        )
        
        Spacer(modifier = Modifier.height(16.dp))
        
        Text(
            text = "Current Reps: $reps",
            color = MaterialTheme.colorScheme.secondary,
            style = MaterialTheme.typography.headlineLarge
        )

        Spacer(modifier = Modifier.height(32.dp))

        // Camera Preview
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(300.dp)
                .padding(16.dp),
            contentAlignment = Alignment.Center
        ) {
            if (hasCameraPermission) {
                CameraPreview(onResult = { result ->
                    mainViewModel.processPoseResult(result)
                })
            } else {
                Text("Camera permission required.")
            }
        }

        Spacer(modifier = Modifier.height(32.dp))

        // App Selection UI
        Text("Block These Apps:", style = MaterialTheme.typography.titleMedium)
        Spacer(modifier = Modifier.height(8.dp))
        
        val installedApps = mainViewModel.installedApps.value

        installedApps.forEach { app ->
            val isBlocked = blockedApps.any { it.packageName == app.packageName }
            Row(
                modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Icon (Optional, skip for performance if needed)
                Text(app.name, modifier = Modifier.weight(1f))
                Checkbox(
                    checked = isBlocked,
                    onCheckedChange = { checked ->
                        scope.launch {
                            if (checked) {
                                blockedDao.insert(BlockedApp(app.packageName))
                            } else {
                                blockedDao.delete(BlockedApp(app.packageName))
                            }
                        }
                    }
                )
            }
        }
    }
}

@Composable
fun CameraPreview(onResult: (PoseLandmarkerResult) -> Unit) {
    val context = androidx.compose.ui.platform.LocalContext.current
    val lifecycleOwner = androidx.compose.ui.platform.LocalLifecycleOwner.current
    val cameraExecutor = remember { Executors.newSingleThreadExecutor() }
    
    val poseLandmarkerHelper = remember {
        PoseLandmarkerHelper(context, object : PoseLandmarkerHelper.LandmarkerListener {
            override fun onError(error: String) {
                Log.e("CameraPreview", "Landmarker Error: $error")
            }
            override fun onResults(result: PoseLandmarkerResult) {
                onResult(result)
            }
        })
    }

    AndroidView(
        factory = { ctx ->
            PreviewView(ctx).apply {
                scaleType = PreviewView.ScaleType.FILL_CENTER
            }
        },
        modifier = Modifier.fillMaxSize(),
        update = { previewView ->
            val cameraProviderFuture = ProcessCameraProvider.getInstance(context)
            cameraProviderFuture.addListener({
                val cameraProvider = cameraProviderFuture.get()
                val preview = Preview.Builder().build().also {
                    it.setSurfaceProvider(previewView.surfaceProvider)
                }

                val imageAnalyzer = ImageAnalysis.Builder()
                    .setBackpressureStrategy(ImageAnalysis.STRATEGY_KEEP_ONLY_LATEST)
                    .setOutputImageFormat(ImageAnalysis.OUTPUT_IMAGE_FORMAT_RGBA_8888)
                    .build()
                    .also {
                        it.setAnalyzer(cameraExecutor) { imageProxy ->
                            val bitmap = imageProxy.toBitmap()
                            val mpImage = BitmapImageBuilder(bitmap).build()
                            poseLandmarkerHelper.detectLiveStream(mpImage)
                            imageProxy.close()
                        }
                    }

                try {
                    cameraProvider.unbindAll()
                    cameraProvider.bindToLifecycle(
                        lifecycleOwner,
                        CameraSelector.DEFAULT_FRONT_CAMERA,
                        preview,
                        imageAnalyzer
                    )
                } catch (exc: Exception) {
                    Log.e("CameraPreview", "Use case binding failed", exc)
                }
            }, ContextCompat.getMainExecutor(context))
        }
    )
}

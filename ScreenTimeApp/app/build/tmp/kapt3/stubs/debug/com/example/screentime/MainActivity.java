package com.example.screentime;

import android.os.Bundle;
import androidx.activity.ComponentActivity;
import androidx.compose.foundation.layout.*;
import androidx.compose.material3.*;
import androidx.compose.runtime.*;
import androidx.compose.runtime.State;
import androidx.compose.ui.Alignment;
import androidx.compose.ui.Modifier;
import android.content.Intent;
import android.net.Uri;
import android.os.PowerManager;
import android.provider.Settings;
import androidx.activity.result.contract.ActivityResultContracts;
import android.Manifest;
import android.content.pm.PackageManager;
import androidx.core.content.ContextCompat;
import com.example.screentime.db.AppDatabase;
import kotlinx.coroutines.Dispatchers;
import androidx.lifecycle.ViewModel;
import androidx.camera.view.PreviewView;
import com.example.screentime.PoseLandmarkerHelper;
import com.google.mediapipe.tasks.vision.poselandmarker.PoseLandmarkerResult;
import com.google.mediapipe.framework.image.BitmapImageBuilder;
import com.google.mediapipe.framework.image.MPImage;
import android.graphics.Bitmap;
import androidx.camera.core.*;
import androidx.camera.lifecycle.ProcessCameraProvider;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import android.util.Log;
import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import android.content.Context;
import android.content.pm.ApplicationInfo;
import android.graphics.drawable.Drawable;
import com.example.screentime.ExerciseCredit;

@kotlin.Metadata(mv = {1, 9, 0}, k = 1, xi = 48, d1 = {"\u0000\u0018\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0010\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\u0018\u00002\u00020\u0001B\u0005\u00a2\u0006\u0002\u0010\u0002J\u0012\u0010\u0003\u001a\u00020\u00042\b\u0010\u0005\u001a\u0004\u0018\u00010\u0006H\u0014\u00a8\u0006\u0007"}, d2 = {"Lcom/example/screentime/MainActivity;", "Landroidx/activity/ComponentActivity;", "()V", "onCreate", "", "savedInstanceState", "Landroid/os/Bundle;", "app_debug"})
public final class MainActivity extends androidx.activity.ComponentActivity {
    
    public MainActivity() {
        super();
    }
    
    @java.lang.Override
    protected void onCreate(@org.jetbrains.annotations.Nullable
    android.os.Bundle savedInstanceState) {
    }
}
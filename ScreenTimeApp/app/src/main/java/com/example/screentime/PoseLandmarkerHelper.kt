package com.example.screentime

import android.content.Context
import android.os.SystemClock
import android.util.Log
import com.google.mediapipe.framework.image.MPImage
import com.google.mediapipe.tasks.core.BaseOptions
import com.google.mediapipe.tasks.core.Delegate
import com.google.mediapipe.tasks.vision.core.RunningMode
import com.google.mediapipe.tasks.vision.poselandmarker.PoseLandmarker
import com.google.mediapipe.tasks.vision.poselandmarker.PoseLandmarkerResult

class PoseLandmarkerHelper(
    val context: Context,
    val listener: LandmarkerListener
) {
    private var poseLandmarker: PoseLandmarker? = null

    init {
        setupPoseLandmarker()
    }

    private fun setupPoseLandmarker() {
        val baseOptionsBuilder = BaseOptions.builder()
            .setDelegate(Delegate.GPU)
            .setModelAssetPath("pose_landmarker_lite.task")

        val optionsBuilder = PoseLandmarker.PoseLandmarkerOptions.builder()
            .setBaseOptions(baseOptionsBuilder.build())
            .setRunningMode(RunningMode.LIVE_STREAM)
            .setResultListener(this::returnLivestreamResult)
            .setErrorListener(this::returnLivestreamError)

        val options = optionsBuilder.build()
        poseLandmarker = PoseLandmarker.createFromOptions(context, options)
    }

    fun detectLiveStream(image: MPImage) {
        val frameTime = SystemClock.uptimeMillis()
        poseLandmarker?.detectAsync(image, frameTime)
    }

    private fun returnLivestreamResult(
        result: PoseLandmarkerResult,
        input: MPImage
    ) {
        listener.onResults(result)
    }

    private fun returnLivestreamError(error: RuntimeException) {
        listener.onError(error.message ?: "Unknown error")
    }

    interface LandmarkerListener {
        fun onError(error: String)
        fun onResults(result: PoseLandmarkerResult)
    }
}

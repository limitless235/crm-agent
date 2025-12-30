package com.example.screentime

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import com.google.mediapipe.tasks.vision.poselandmarker.PoseLandmarkerResult

class RepCounter {
    private val _repCount = MutableLiveData<Int>(0)
    val repCount: LiveData<Int> = _repCount

    private var isDown = false
    private val threshold = 0.05f // Relative distance threshold for "Down" state

    fun processResult(result: PoseLandmarkerResult) {
        val landmarks = result.landmarks()
        if (landmarks.isEmpty()) return

        val poseLandmarks = landmarks[0]
        
        // Landmark indices: Nose = 0, Left Shoulder = 11, Right Shoulder = 12
        val nose = poseLandmarks[0]
        val leftShoulder = poseLandmarks[11]
        val rightShoulder = poseLandmarks[12]

        val shouldersY = (leftShoulder.y() + rightShoulder.y()) / 2
        val noseY = nose.y()

        // In MediaPipe, Y increases downwards.
        // For pushups/squats, "Down" means nose is closer to or below shoulders (higher Y).
        
        val relativePos = noseY - shouldersY

        if (!isDown && relativePos > threshold) {
            isDown = true
        } else if (isDown && relativePos < 0) {
            isDown = false
            _repCount.postValue((_repCount.value ?: 0) + 1)
        }
    }

    fun reset() {
        _repCount.postValue(0)
        isDown = false
    }
}

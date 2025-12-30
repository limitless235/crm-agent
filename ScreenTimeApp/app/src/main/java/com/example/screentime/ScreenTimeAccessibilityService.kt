package com.example.screentime

import android.accessibilityservice.AccessibilityService
import android.accessibilityservice.AccessibilityServiceInfo
import android.os.Build
import android.util.Log
import android.view.accessibility.AccessibilityEvent
import androidx.core.app.NotificationCompat
import android.app.NotificationChannel
import android.app.NotificationManager
import android.view.WindowManager
import android.view.Gravity
import android.graphics.PixelFormat
import android.widget.TextView
import android.graphics.Color
import android.view.View
import com.example.screentime.db.AppDatabase
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.flow.first

class ScreenTimeAccessibilityService : AccessibilityService() {
    private var windowManager: WindowManager? = null
    private var overlayView: View? = null
    private val serviceScope = CoroutineScope(Dispatchers.Main)

    override fun onServiceConnected() {
        super.onServiceConnected()
        Log.d("ScreenTimeService", "Service Connected")
        
        windowManager = getSystemService(WINDOW_SERVICE) as WindowManager

        // Low-memory footprint configuration
        val info = AccessibilityServiceInfo()
        info.eventTypes = AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED
        info.feedbackType = AccessibilityServiceInfo.FEEDBACK_GENERIC
        info.notificationTimeout = 100
        info.flags = AccessibilityServiceInfo.FLAG_INCLUDE_NOT_IMPORTANT_VIEWS
        this.serviceInfo = info

        startForegroundService()
    }

    private fun startForegroundService() {
        val channelId = "screen_time_service_channel"
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                channelId,
                "Screen Time Service",
                NotificationManager.IMPORTANCE_LOW
            )
            val manager = getSystemService(NotificationManager::class.java)
            manager.createNotificationChannel(channel)
        }

        val notification = NotificationCompat.Builder(this, channelId)
            .setContentTitle("Screen Time Monitor")
            .setContentText("Monitoring app usage...")
            .setSmallIcon(android.R.drawable.ic_dialog_info)
            .setOngoing(true) // Sticky notification
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .build()

        startForeground(1, notification)
    }

    private fun showOverlay() {
        if (overlayView != null) return

        val params = WindowManager.LayoutParams(
            WindowManager.LayoutParams.MATCH_PARENT,
            WindowManager.LayoutParams.MATCH_PARENT,
            WindowManager.LayoutParams.TYPE_ACCESSIBILITY_OVERLAY,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or WindowManager.LayoutParams.FLAG_LAYOUT_IN_SCREEN,
            PixelFormat.TRANSLUCENT
        )
        params.gravity = Gravity.CENTER

        val textView = TextView(this).apply {
            text = "Exercise Lock: Add credits to unlock!"
            setTextColor(Color.WHITE)
            setBackgroundColor(Color.parseColor("#CC000000"))
            gravity = Gravity.CENTER
            textSize = 24f
        }

        overlayView = textView
        windowManager?.addView(overlayView, params)
    }

    private fun hideOverlay() {
        overlayView?.let {
            windowManager?.removeView(it)
            overlayView = null
        }
    }

    override fun onAccessibilityEvent(event: AccessibilityEvent) {
        if (event.eventType == AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED) {
            val packageName = event.packageName?.toString() ?: return
            Log.d("ScreenTimeService", "App launched: $packageName")
            
            checkAppAndLock(packageName)
        }
    }

    private fun checkAppAndLock(packageName: String) {
        serviceScope.launch {
            val db = AppDatabase.getDatabase(applicationContext)
            val blockedApps = db.blockedAppDao().getAllBlockedApps().first()
            val isBlocked = blockedApps.any { it.packageName == packageName }

            if (isBlocked) {
                val credits = db.exerciseCreditDao().getLatestCredits().first()
                val creditsInSeconds = credits?.creditsInSeconds ?: 0

                if (creditsInSeconds <= 0) {
                    showOverlay()
                } else {
                    hideOverlay()
                }
            } else {
                // If it's not a blocked app, we might want to hide the overlay if it was showing
                // but usually the overlay only shows over blocked apps.
                // However, switching from Instagram to Home should hide it.
                hideOverlay()
            }
        }
    }

    override fun onInterrupt() {
        Log.d("ScreenTimeService", "Service Interrupted")
    }
}

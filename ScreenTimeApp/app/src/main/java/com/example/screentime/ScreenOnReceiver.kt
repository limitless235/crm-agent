package com.example.screentime

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.util.Log

class ScreenOnReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action == Intent.ACTION_SCREEN_ON) {
            Log.d("ScreenOnReceiver", "Screen turned on!")
            // You can trigger some logic here, like checking credits
        }
    }
}

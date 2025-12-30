package com.example.screentime

import android.os.Build

class SmartCoachEngine {

    /**
     * Generates a motivational message based on credits and the target app.
     * Optimization: Lightweight logic-tree ensures no UI blocking on the main thread,
     * specifically targeting performance-sensitive devices like the Galaxy A12.
     */
    fun getMotivationalMessage(creditsInSeconds: Long, targetApp: String): String {
        val isGalaxyA12 = Build.MODEL.contains("A12", ignoreCase = true)
        
        // Logic-tree for motivational text
        return when {
            creditsInSeconds <= 0 -> {
                "Time to move! Reach 30 seconds for a quick peak at $targetApp."
            }
            creditsInSeconds < 300 -> {
                val repsNeeded = ((300 - creditsInSeconds) / 5).coerceAtLeast(1)
                "You're $repsNeeded reps away from 5 mins of $targetApp!"
            }
            creditsInSeconds < 600 -> {
                "Great work! You've earned enough for a good session on $targetApp."
            }
            else -> {
                "Champion! You've got plenty of $targetApp time. Keep it up!"
            }
        }
    }
}

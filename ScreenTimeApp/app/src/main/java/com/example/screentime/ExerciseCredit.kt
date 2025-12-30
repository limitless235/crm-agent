package com.example.screentime

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "exercise_credits")
data class ExerciseCredit(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val creditsInSeconds: Long
)

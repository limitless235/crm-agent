package com.example.screentime.db

import androidx.room.*
import com.example.screentime.ExerciseCredit
import kotlinx.coroutines.flow.Flow

@Dao
interface ExerciseCreditDao {
    @Query("SELECT * FROM exercise_credits ORDER BY id DESC LIMIT 1")
    fun getLatestCredits(): Flow<ExerciseCredit?>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(credit: ExerciseCredit)

    @Query("DELETE FROM exercise_credits")
    suspend fun deleteAll()
}

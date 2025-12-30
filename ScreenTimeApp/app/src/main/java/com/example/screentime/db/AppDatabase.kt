package com.example.screentime.db

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import com.example.screentime.ExerciseCredit
import com.example.screentime.BlockedApp

@Database(entities = [ExerciseCredit::class, BlockedApp::class], version = 2, exportSchema = false)
abstract class AppDatabase : RoomDatabase() {
    abstract fun exerciseCreditDao(): ExerciseCreditDao
    abstract fun blockedAppDao(): BlockedAppDao

    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null

        fun getDatabase(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "screentime_database"
                )
                .fallbackToDestructiveMigration()
                .build()
                INSTANCE = instance
                instance
            }
        }
    }
}

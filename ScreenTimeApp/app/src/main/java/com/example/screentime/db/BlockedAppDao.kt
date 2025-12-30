package com.example.screentime.db

import androidx.room.*
import com.example.screentime.BlockedApp
import kotlinx.coroutines.flow.Flow

@Dao
interface BlockedAppDao {
    @Query("SELECT * FROM blocked_apps")
    fun getAllBlockedApps(): Flow<List<BlockedApp>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(app: BlockedApp)

    @Delete
    suspend fun delete(app: BlockedApp)
}

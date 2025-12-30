package com.example.screentime.db;

import androidx.annotation.NonNull;
import androidx.room.DatabaseConfiguration;
import androidx.room.InvalidationTracker;
import androidx.room.RoomDatabase;
import androidx.room.RoomOpenHelper;
import androidx.room.migration.AutoMigrationSpec;
import androidx.room.migration.Migration;
import androidx.room.util.DBUtil;
import androidx.room.util.TableInfo;
import androidx.sqlite.db.SupportSQLiteDatabase;
import androidx.sqlite.db.SupportSQLiteOpenHelper;
import java.lang.Class;
import java.lang.Override;
import java.lang.String;
import java.lang.SuppressWarnings;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import javax.annotation.processing.Generated;

@Generated("androidx.room.RoomProcessor")
@SuppressWarnings({"unchecked", "deprecation"})
public final class AppDatabase_Impl extends AppDatabase {
  private volatile ExerciseCreditDao _exerciseCreditDao;

  private volatile BlockedAppDao _blockedAppDao;

  @Override
  @NonNull
  protected SupportSQLiteOpenHelper createOpenHelper(@NonNull final DatabaseConfiguration config) {
    final SupportSQLiteOpenHelper.Callback _openCallback = new RoomOpenHelper(config, new RoomOpenHelper.Delegate(2) {
      @Override
      public void createAllTables(@NonNull final SupportSQLiteDatabase db) {
        db.execSQL("CREATE TABLE IF NOT EXISTS `exercise_credits` (`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, `creditsInSeconds` INTEGER NOT NULL)");
        db.execSQL("CREATE TABLE IF NOT EXISTS `blocked_apps` (`packageName` TEXT NOT NULL, PRIMARY KEY(`packageName`))");
        db.execSQL("CREATE TABLE IF NOT EXISTS room_master_table (id INTEGER PRIMARY KEY,identity_hash TEXT)");
        db.execSQL("INSERT OR REPLACE INTO room_master_table (id,identity_hash) VALUES(42, '6bcc5e58703b1ed161ef3692e283da8e')");
      }

      @Override
      public void dropAllTables(@NonNull final SupportSQLiteDatabase db) {
        db.execSQL("DROP TABLE IF EXISTS `exercise_credits`");
        db.execSQL("DROP TABLE IF EXISTS `blocked_apps`");
        final List<? extends RoomDatabase.Callback> _callbacks = mCallbacks;
        if (_callbacks != null) {
          for (RoomDatabase.Callback _callback : _callbacks) {
            _callback.onDestructiveMigration(db);
          }
        }
      }

      @Override
      public void onCreate(@NonNull final SupportSQLiteDatabase db) {
        final List<? extends RoomDatabase.Callback> _callbacks = mCallbacks;
        if (_callbacks != null) {
          for (RoomDatabase.Callback _callback : _callbacks) {
            _callback.onCreate(db);
          }
        }
      }

      @Override
      public void onOpen(@NonNull final SupportSQLiteDatabase db) {
        mDatabase = db;
        internalInitInvalidationTracker(db);
        final List<? extends RoomDatabase.Callback> _callbacks = mCallbacks;
        if (_callbacks != null) {
          for (RoomDatabase.Callback _callback : _callbacks) {
            _callback.onOpen(db);
          }
        }
      }

      @Override
      public void onPreMigrate(@NonNull final SupportSQLiteDatabase db) {
        DBUtil.dropFtsSyncTriggers(db);
      }

      @Override
      public void onPostMigrate(@NonNull final SupportSQLiteDatabase db) {
      }

      @Override
      @NonNull
      public RoomOpenHelper.ValidationResult onValidateSchema(
          @NonNull final SupportSQLiteDatabase db) {
        final HashMap<String, TableInfo.Column> _columnsExerciseCredits = new HashMap<String, TableInfo.Column>(2);
        _columnsExerciseCredits.put("id", new TableInfo.Column("id", "INTEGER", true, 1, null, TableInfo.CREATED_FROM_ENTITY));
        _columnsExerciseCredits.put("creditsInSeconds", new TableInfo.Column("creditsInSeconds", "INTEGER", true, 0, null, TableInfo.CREATED_FROM_ENTITY));
        final HashSet<TableInfo.ForeignKey> _foreignKeysExerciseCredits = new HashSet<TableInfo.ForeignKey>(0);
        final HashSet<TableInfo.Index> _indicesExerciseCredits = new HashSet<TableInfo.Index>(0);
        final TableInfo _infoExerciseCredits = new TableInfo("exercise_credits", _columnsExerciseCredits, _foreignKeysExerciseCredits, _indicesExerciseCredits);
        final TableInfo _existingExerciseCredits = TableInfo.read(db, "exercise_credits");
        if (!_infoExerciseCredits.equals(_existingExerciseCredits)) {
          return new RoomOpenHelper.ValidationResult(false, "exercise_credits(com.example.screentime.ExerciseCredit).\n"
                  + " Expected:\n" + _infoExerciseCredits + "\n"
                  + " Found:\n" + _existingExerciseCredits);
        }
        final HashMap<String, TableInfo.Column> _columnsBlockedApps = new HashMap<String, TableInfo.Column>(1);
        _columnsBlockedApps.put("packageName", new TableInfo.Column("packageName", "TEXT", true, 1, null, TableInfo.CREATED_FROM_ENTITY));
        final HashSet<TableInfo.ForeignKey> _foreignKeysBlockedApps = new HashSet<TableInfo.ForeignKey>(0);
        final HashSet<TableInfo.Index> _indicesBlockedApps = new HashSet<TableInfo.Index>(0);
        final TableInfo _infoBlockedApps = new TableInfo("blocked_apps", _columnsBlockedApps, _foreignKeysBlockedApps, _indicesBlockedApps);
        final TableInfo _existingBlockedApps = TableInfo.read(db, "blocked_apps");
        if (!_infoBlockedApps.equals(_existingBlockedApps)) {
          return new RoomOpenHelper.ValidationResult(false, "blocked_apps(com.example.screentime.BlockedApp).\n"
                  + " Expected:\n" + _infoBlockedApps + "\n"
                  + " Found:\n" + _existingBlockedApps);
        }
        return new RoomOpenHelper.ValidationResult(true, null);
      }
    }, "6bcc5e58703b1ed161ef3692e283da8e", "13cef7fe344569790c1c93cfcf479f4a");
    final SupportSQLiteOpenHelper.Configuration _sqliteConfig = SupportSQLiteOpenHelper.Configuration.builder(config.context).name(config.name).callback(_openCallback).build();
    final SupportSQLiteOpenHelper _helper = config.sqliteOpenHelperFactory.create(_sqliteConfig);
    return _helper;
  }

  @Override
  @NonNull
  protected InvalidationTracker createInvalidationTracker() {
    final HashMap<String, String> _shadowTablesMap = new HashMap<String, String>(0);
    final HashMap<String, Set<String>> _viewTables = new HashMap<String, Set<String>>(0);
    return new InvalidationTracker(this, _shadowTablesMap, _viewTables, "exercise_credits","blocked_apps");
  }

  @Override
  public void clearAllTables() {
    super.assertNotMainThread();
    final SupportSQLiteDatabase _db = super.getOpenHelper().getWritableDatabase();
    try {
      super.beginTransaction();
      _db.execSQL("DELETE FROM `exercise_credits`");
      _db.execSQL("DELETE FROM `blocked_apps`");
      super.setTransactionSuccessful();
    } finally {
      super.endTransaction();
      _db.query("PRAGMA wal_checkpoint(FULL)").close();
      if (!_db.inTransaction()) {
        _db.execSQL("VACUUM");
      }
    }
  }

  @Override
  @NonNull
  protected Map<Class<?>, List<Class<?>>> getRequiredTypeConverters() {
    final HashMap<Class<?>, List<Class<?>>> _typeConvertersMap = new HashMap<Class<?>, List<Class<?>>>();
    _typeConvertersMap.put(ExerciseCreditDao.class, ExerciseCreditDao_Impl.getRequiredConverters());
    _typeConvertersMap.put(BlockedAppDao.class, BlockedAppDao_Impl.getRequiredConverters());
    return _typeConvertersMap;
  }

  @Override
  @NonNull
  public Set<Class<? extends AutoMigrationSpec>> getRequiredAutoMigrationSpecs() {
    final HashSet<Class<? extends AutoMigrationSpec>> _autoMigrationSpecsSet = new HashSet<Class<? extends AutoMigrationSpec>>();
    return _autoMigrationSpecsSet;
  }

  @Override
  @NonNull
  public List<Migration> getAutoMigrations(
      @NonNull final Map<Class<? extends AutoMigrationSpec>, AutoMigrationSpec> autoMigrationSpecs) {
    final List<Migration> _autoMigrations = new ArrayList<Migration>();
    return _autoMigrations;
  }

  @Override
  public ExerciseCreditDao exerciseCreditDao() {
    if (_exerciseCreditDao != null) {
      return _exerciseCreditDao;
    } else {
      synchronized(this) {
        if(_exerciseCreditDao == null) {
          _exerciseCreditDao = new ExerciseCreditDao_Impl(this);
        }
        return _exerciseCreditDao;
      }
    }
  }

  @Override
  public BlockedAppDao blockedAppDao() {
    if (_blockedAppDao != null) {
      return _blockedAppDao;
    } else {
      synchronized(this) {
        if(_blockedAppDao == null) {
          _blockedAppDao = new BlockedAppDao_Impl(this);
        }
        return _blockedAppDao;
      }
    }
  }
}

package com.example.screentime.db;

import android.database.Cursor;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.room.CoroutinesRoom;
import androidx.room.EntityDeletionOrUpdateAdapter;
import androidx.room.EntityInsertionAdapter;
import androidx.room.RoomDatabase;
import androidx.room.RoomSQLiteQuery;
import androidx.room.util.CursorUtil;
import androidx.room.util.DBUtil;
import androidx.sqlite.db.SupportSQLiteStatement;
import com.example.screentime.BlockedApp;
import java.lang.Class;
import java.lang.Exception;
import java.lang.Object;
import java.lang.Override;
import java.lang.String;
import java.lang.SuppressWarnings;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.Callable;
import javax.annotation.processing.Generated;
import kotlin.Unit;
import kotlin.coroutines.Continuation;
import kotlinx.coroutines.flow.Flow;

@Generated("androidx.room.RoomProcessor")
@SuppressWarnings({"unchecked", "deprecation"})
public final class BlockedAppDao_Impl implements BlockedAppDao {
  private final RoomDatabase __db;

  private final EntityInsertionAdapter<BlockedApp> __insertionAdapterOfBlockedApp;

  private final EntityDeletionOrUpdateAdapter<BlockedApp> __deletionAdapterOfBlockedApp;

  public BlockedAppDao_Impl(@NonNull final RoomDatabase __db) {
    this.__db = __db;
    this.__insertionAdapterOfBlockedApp = new EntityInsertionAdapter<BlockedApp>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "INSERT OR REPLACE INTO `blocked_apps` (`packageName`) VALUES (?)";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement,
          @Nullable final BlockedApp entity) {
        if (entity.getPackageName() == null) {
          statement.bindNull(1);
        } else {
          statement.bindString(1, entity.getPackageName());
        }
      }
    };
    this.__deletionAdapterOfBlockedApp = new EntityDeletionOrUpdateAdapter<BlockedApp>(__db) {
      @Override
      @NonNull
      protected String createQuery() {
        return "DELETE FROM `blocked_apps` WHERE `packageName` = ?";
      }

      @Override
      protected void bind(@NonNull final SupportSQLiteStatement statement,
          @Nullable final BlockedApp entity) {
        if (entity.getPackageName() == null) {
          statement.bindNull(1);
        } else {
          statement.bindString(1, entity.getPackageName());
        }
      }
    };
  }

  @Override
  public Object insert(final BlockedApp app, final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        __db.beginTransaction();
        try {
          __insertionAdapterOfBlockedApp.insert(app);
          __db.setTransactionSuccessful();
          return Unit.INSTANCE;
        } finally {
          __db.endTransaction();
        }
      }
    }, $completion);
  }

  @Override
  public Object delete(final BlockedApp app, final Continuation<? super Unit> $completion) {
    return CoroutinesRoom.execute(__db, true, new Callable<Unit>() {
      @Override
      @NonNull
      public Unit call() throws Exception {
        __db.beginTransaction();
        try {
          __deletionAdapterOfBlockedApp.handle(app);
          __db.setTransactionSuccessful();
          return Unit.INSTANCE;
        } finally {
          __db.endTransaction();
        }
      }
    }, $completion);
  }

  @Override
  public Flow<List<BlockedApp>> getAllBlockedApps() {
    final String _sql = "SELECT * FROM blocked_apps";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 0);
    return CoroutinesRoom.createFlow(__db, false, new String[] {"blocked_apps"}, new Callable<List<BlockedApp>>() {
      @Override
      @NonNull
      public List<BlockedApp> call() throws Exception {
        final Cursor _cursor = DBUtil.query(__db, _statement, false, null);
        try {
          final int _cursorIndexOfPackageName = CursorUtil.getColumnIndexOrThrow(_cursor, "packageName");
          final List<BlockedApp> _result = new ArrayList<BlockedApp>(_cursor.getCount());
          while (_cursor.moveToNext()) {
            final BlockedApp _item;
            final String _tmpPackageName;
            if (_cursor.isNull(_cursorIndexOfPackageName)) {
              _tmpPackageName = null;
            } else {
              _tmpPackageName = _cursor.getString(_cursorIndexOfPackageName);
            }
            _item = new BlockedApp(_tmpPackageName);
            _result.add(_item);
          }
          return _result;
        } finally {
          _cursor.close();
        }
      }

      @Override
      protected void finalize() {
        _statement.release();
      }
    });
  }

  @NonNull
  public static List<Class<?>> getRequiredConverters() {
    return Collections.emptyList();
  }
}

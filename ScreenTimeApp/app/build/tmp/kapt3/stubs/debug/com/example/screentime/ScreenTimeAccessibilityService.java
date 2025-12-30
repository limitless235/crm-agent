package com.example.screentime;

import android.accessibilityservice.AccessibilityService;
import android.accessibilityservice.AccessibilityServiceInfo;
import android.os.Build;
import android.util.Log;
import android.view.accessibility.AccessibilityEvent;
import androidx.core.app.NotificationCompat;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.view.WindowManager;
import android.view.Gravity;
import android.graphics.PixelFormat;
import android.widget.TextView;
import android.graphics.Color;
import android.view.View;
import com.example.screentime.db.AppDatabase;
import kotlinx.coroutines.Dispatchers;

@kotlin.Metadata(mv = {1, 9, 0}, k = 1, xi = 48, d1 = {"\u00004\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u0002\n\u0000\n\u0002\u0010\u000e\n\u0002\b\u0003\n\u0002\u0018\u0002\n\u0002\b\u0005\u0018\u00002\u00020\u0001B\u0005\u00a2\u0006\u0002\u0010\u0002J\u0010\u0010\t\u001a\u00020\n2\u0006\u0010\u000b\u001a\u00020\fH\u0002J\b\u0010\r\u001a\u00020\nH\u0002J\u0010\u0010\u000e\u001a\u00020\n2\u0006\u0010\u000f\u001a\u00020\u0010H\u0016J\b\u0010\u0011\u001a\u00020\nH\u0016J\b\u0010\u0012\u001a\u00020\nH\u0014J\b\u0010\u0013\u001a\u00020\nH\u0002J\b\u0010\u0014\u001a\u00020\nH\u0002R\u0010\u0010\u0003\u001a\u0004\u0018\u00010\u0004X\u0082\u000e\u00a2\u0006\u0002\n\u0000R\u000e\u0010\u0005\u001a\u00020\u0006X\u0082\u0004\u00a2\u0006\u0002\n\u0000R\u0010\u0010\u0007\u001a\u0004\u0018\u00010\bX\u0082\u000e\u00a2\u0006\u0002\n\u0000\u00a8\u0006\u0015"}, d2 = {"Lcom/example/screentime/ScreenTimeAccessibilityService;", "Landroid/accessibilityservice/AccessibilityService;", "()V", "overlayView", "Landroid/view/View;", "serviceScope", "Lkotlinx/coroutines/CoroutineScope;", "windowManager", "Landroid/view/WindowManager;", "checkAppAndLock", "", "packageName", "", "hideOverlay", "onAccessibilityEvent", "event", "Landroid/view/accessibility/AccessibilityEvent;", "onInterrupt", "onServiceConnected", "showOverlay", "startForegroundService", "app_debug"})
public final class ScreenTimeAccessibilityService extends android.accessibilityservice.AccessibilityService {
    @org.jetbrains.annotations.Nullable
    private android.view.WindowManager windowManager;
    @org.jetbrains.annotations.Nullable
    private android.view.View overlayView;
    @org.jetbrains.annotations.NotNull
    private final kotlinx.coroutines.CoroutineScope serviceScope = null;
    
    public ScreenTimeAccessibilityService() {
        super();
    }
    
    @java.lang.Override
    protected void onServiceConnected() {
    }
    
    private final void startForegroundService() {
    }
    
    private final void showOverlay() {
    }
    
    private final void hideOverlay() {
    }
    
    @java.lang.Override
    public void onAccessibilityEvent(@org.jetbrains.annotations.NotNull
    android.view.accessibility.AccessibilityEvent event) {
    }
    
    private final void checkAppAndLock(java.lang.String packageName) {
    }
    
    @java.lang.Override
    public void onInterrupt() {
    }
}
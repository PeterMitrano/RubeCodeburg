package com.google.cloud.android.speech;

import android.hardware.camera2.CameraAccessException;
import android.hardware.camera2.CameraManager;
import android.os.AsyncTask;

public class MorseEmitter extends AsyncTask<Void, Void, Void> {

  private static final long DOT_DELAY = 200;
  private static final long DASH_DELAY = 600;
  private static final long SPACE_DELAY = 800;
  private static final long CHAR_DELAY = 200;
  private final CameraManager cameraManager;
  private final String cameraId;
  private final String morse;

  MorseEmitter(CameraManager cameraManager, String cameraId, String morse) {
    this.cameraManager = cameraManager;
    this.cameraId = cameraId;
    this.morse = morse;
  }

  @Override
  protected Void doInBackground(Void... params) {
    try {
      for (int i = 0; i < morse.length(); i++) {
        char c = morse.charAt(i);
        if (c == '.') {
          dot();
        }
        else if (c == '-') {
          dash();
        }
        else if (c == ' ') {
          space();
        }
      }
    } catch (InterruptedException | CameraAccessException e) {
      e.printStackTrace();
    }
    return null;
  }

  private void dot() throws CameraAccessException, InterruptedException {
    cameraManager.setTorchMode(cameraId, true);
    Thread.sleep(DOT_DELAY);
    cameraManager.setTorchMode(cameraId, false);
    Thread.sleep(CHAR_DELAY);
  }

  private void dash() throws CameraAccessException, InterruptedException {
    cameraManager.setTorchMode(cameraId, true);
    Thread.sleep(DASH_DELAY);
    cameraManager.setTorchMode(cameraId, false);
    Thread.sleep(CHAR_DELAY);
  }

  private void space() throws CameraAccessException, InterruptedException {
    Thread.sleep(SPACE_DELAY);
    Thread.sleep(CHAR_DELAY); // not sure if I want this
  }
}

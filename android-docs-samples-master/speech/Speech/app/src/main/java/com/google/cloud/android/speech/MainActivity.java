/*
 * Copyright 2016 Google Inc. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.google.cloud.android.speech;

import android.Manifest;
import android.content.ComponentName;
import android.content.Intent;
import android.content.ServiceConnection;
import android.content.pm.PackageManager;
import android.content.res.Resources;
import android.hardware.camera2.CameraAccessException;
import android.hardware.camera2.CameraManager;
import android.os.Bundle;
import android.os.IBinder;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.res.ResourcesCompat;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.LinearLayoutManager;
import android.support.v7.widget.RecyclerView;
import android.support.v7.widget.Toolbar;
import android.text.TextUtils;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.google.cloud.android.speech.MessageDialogFragment.Listener;
import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.util.ArrayList;
import org.json.JSONException;
import org.json.JSONObject;


public class MainActivity extends AppCompatActivity implements Listener, OnClickListener {

  private static final String FRAGMENT_MESSAGE_DIALOG = "message_dialog";

  private static final String STATE_RESULTS = "results";

  private static final int REQUEST_RECORD_AUDIO_PERMISSION = 1;

  private SpeechService mSpeechService;

  private VoiceRecorder mVoiceRecorder;
  // Resource caches
  private int mColorHearing;
  private int mColorNotHearing;
  // View references
  private TextView mStatus;
  private final VoiceRecorder.Callback mVoiceCallback = new VoiceRecorder.Callback() {

    @Override
    public void onVoiceStart() {
      showStatus(true);
      if (mSpeechService != null) {
        mSpeechService.startRecognizing(mVoiceRecorder.getSampleRate());
      }
    }

    @Override
    public void onVoice(byte[] data, int size) {
      if (mSpeechService != null) {
        mSpeechService.recognize(data, size);
      }
    }

    @Override
    public void onVoiceEnd() {
      showStatus(false);
      if (mSpeechService != null) {
        mSpeechService.finishRecognizing();
      }
    }

  };
  private Button startButton;
  private TextView mText;
  private ResultAdapter mAdapter;
  private RecyclerView mRecyclerView;
  private final SpeechService.Listener mSpeechServiceListener =
      new SpeechService.Listener() {
        @Override
        public void onSpeechRecognized(final String text, final boolean isFinal) {
          if (isFinal) {
            mVoiceRecorder.dismiss();
            stopVoiceRecorder();
          }
          if (mText != null && !TextUtils.isEmpty(text)) {
            runOnUiThread(new Runnable() {
              @Override
              public void run() {
                if (isFinal) {
                  mText.setText(null);
                  mAdapter.addResult(text);
                  // TODO: translate to french
                  convertToFrenchAndFlashMorse(text);
                  mRecyclerView.smoothScrollToPosition(0);
                } else {
                  mText.setText(text);
                }
              }
            });
          }
        }
      };
  private final ServiceConnection mServiceConnection = new ServiceConnection() {

    @Override
    public void onServiceConnected(ComponentName componentName, IBinder binder) {
      mSpeechService = SpeechService.from(binder);
      mSpeechService.addListener(mSpeechServiceListener);
      mStatus.setVisibility(View.VISIBLE);
    }

    @Override
    public void onServiceDisconnected(ComponentName componentName) {
      mSpeechService = null;
    }

  };

  private void convertToFrenchAndFlashMorse(String text) {
    RequestQueue queue = Volley.newRequestQueue(this);
    String query;
    try {
      query = URLEncoder.encode(text, "utf-8");
    } catch (UnsupportedEncodingException e) {
      e.printStackTrace();
      return;
    }

    String url =
        "https://translation.googleapis.com/language/translate/v2?key=AIzaSyCVXtLKgIoKeVnvdijJ6Wxahc74I5qBCdw&q="
            + query + "&target=fr";

    JsonObjectRequest jsObjRequest = new JsonObjectRequest
        (Request.Method.GET, url, null, new Response.Listener<JSONObject>() {

          @Override
          public void onResponse(JSONObject response) {
            try {
              JSONObject data = response.getJSONObject("data");
              JSONObject translation = data.getJSONArray("translations").getJSONObject(0);
              String french = translation.getString("translatedText");
              Log.e(getClass().toString(), french);
              convertToMorse(french);
            } catch (JSONException e) {
              e.printStackTrace();
            }
          }
        }, new Response.ErrorListener() {

          @Override
          public void onErrorResponse(VolleyError error) {
            error.printStackTrace();
          }
        });
    queue.add(jsObjRequest);
  }

  private void convertToMorse(String french) {
    RequestQueue queue = Volley.newRequestQueue(this);
    String query;
    try {
      query = URLEncoder.encode(french, "utf-8");
    } catch (UnsupportedEncodingException e) {
      e.printStackTrace();
      return;
    }

    String url = "http://api.funtranslations.com/translate/morse.json?text=" + query;

    JsonObjectRequest jsObjRequest = new JsonObjectRequest
        (Request.Method.GET, url, null, new Response.Listener<JSONObject>() {

          @Override
          public void onResponse(JSONObject response) {
            try {
              JSONObject contents = response.getJSONObject("contents");
              String morse = contents.getString("translated");
              Log.e(getClass().toString(), morse);
              flashMorse(morse);

            } catch (JSONException e) {
              e.printStackTrace();
            }
          }
        }, new Response.ErrorListener() {

          @Override
          public void onErrorResponse(VolleyError error) {
            error.printStackTrace();
          }
        });
    // TODO: renable me
//    queue.add(jsObjRequest);
    flashMorse(".... --- -     -.. --- --. ");
  }

  private void flashMorse(String morse) {
    //TODO: send morse via camera flash
    CameraManager cameraManager = (CameraManager) getApplicationContext()
        .getSystemService(CAMERA_SERVICE);
    try {
      String cameraId = getFrontFacingCameraId(cameraManager);
      if (cameraId != null) {
        MorseEmitter emitter = new MorseEmitter(cameraManager, cameraId, morse);
        emitter.execute();
      }
    } catch (CameraAccessException e) {
      e.printStackTrace();
    }
  }

  String getFrontFacingCameraId(CameraManager cManager) throws CameraAccessException {
//    for(final String cameraId : cManager.getCameraIdList()){
//      CameraCharacteristics characteristics = cManager.getCameraCharacteristics(cameraId);
//      Log.e(getClass().toString(), characteristics.toString());
//      int cOrientation = characteristics.get(CameraCharacteristics.);
//      if(cOrientation == CameraCharacteristics.LENS_FACING_FRONT) {
//        return cameraId;
//      }
//    }

    return "0";
  }

  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_main);

    final Resources resources = getResources();
    final Resources.Theme theme = getTheme();
    mColorHearing = ResourcesCompat.getColor(resources, R.color.status_hearing, theme);
    mColorNotHearing = ResourcesCompat.getColor(resources, R.color.status_not_hearing, theme);

    setSupportActionBar((Toolbar) findViewById(R.id.toolbar));
    mStatus = (TextView) findViewById(R.id.status);
    mText = (TextView) findViewById(R.id.text);

    mRecyclerView = (RecyclerView) findViewById(R.id.recycler_view);
    mRecyclerView.setLayoutManager(new LinearLayoutManager(this));
    final ArrayList<String> results = savedInstanceState == null ? null :
        savedInstanceState.getStringArrayList(STATE_RESULTS);
    mAdapter = new ResultAdapter(results);
    mRecyclerView.setAdapter(mAdapter);

    startButton = (Button) findViewById(R.id.start_recording);
    startButton.setOnClickListener(this);
  }

  @Override
  protected void onStart() {
    super.onStart();

    // Prepare Cloud Speech API
    bindService(new Intent(this, SpeechService.class), mServiceConnection, BIND_AUTO_CREATE);

    // Start listening to voices
    if (ActivityCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO)
        == PackageManager.PERMISSION_GRANTED) {
//      startVoiceRecorder();
    } else if (ActivityCompat.shouldShowRequestPermissionRationale(this,
        Manifest.permission.RECORD_AUDIO)) {
      showPermissionMessageDialog();
    } else {
      ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.RECORD_AUDIO},
          REQUEST_RECORD_AUDIO_PERMISSION);
    }
  }

  @Override
  protected void onStop() {
    // Stop listening to voice
    stopVoiceRecorder();

    // Stop Cloud Speech API
    mSpeechService.removeListener(mSpeechServiceListener);
    unbindService(mServiceConnection);
    mSpeechService = null;

    super.onStop();
  }

  @Override
  protected void onSaveInstanceState(Bundle outState) {
    super.onSaveInstanceState(outState);
    if (mAdapter != null) {
      outState.putStringArrayList(STATE_RESULTS, mAdapter.getResults());
    }
  }

  @Override
  public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions,
      @NonNull int[] grantResults) {
    if (requestCode == REQUEST_RECORD_AUDIO_PERMISSION) {
      if (permissions.length == 1 && grantResults.length == 1
          && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
//        startVoiceRecorder();
      } else {
        showPermissionMessageDialog();
      }
    } else {
      super.onRequestPermissionsResult(requestCode, permissions, grantResults);
    }
  }

  @Override
  public boolean onCreateOptionsMenu(Menu menu) {
    getMenuInflater().inflate(R.menu.main, menu);
    return true;
  }

  @Override
  public boolean onOptionsItemSelected(MenuItem item) {
    switch (item.getItemId()) {
      case R.id.action_file:
        mSpeechService.recognizeInputStream(getResources().openRawResource(R.raw.audio));
        return true;
      default:
        return super.onOptionsItemSelected(item);
    }
  }

  private void startVoiceRecorder() {
    if (mVoiceRecorder != null) {
      mVoiceRecorder.stop();
    }
    mVoiceRecorder = new VoiceRecorder(mVoiceCallback);
    mVoiceRecorder.start();
  }

  private void stopVoiceRecorder() {
    if (mVoiceRecorder != null) {
      mVoiceRecorder.stop();
      mVoiceRecorder = null;
    }
  }

  private void showPermissionMessageDialog() {
    MessageDialogFragment
        .newInstance(getString(R.string.permission_message))
        .show(getSupportFragmentManager(), FRAGMENT_MESSAGE_DIALOG);
  }

  private void showStatus(final boolean hearingVoice) {
    runOnUiThread(new Runnable() {
      @Override
      public void run() {
        mStatus.setTextColor(hearingVoice ? mColorHearing : mColorNotHearing);
      }
    });
  }

  @Override
  public void onMessageDialogDismissed() {
    ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.RECORD_AUDIO},
        REQUEST_RECORD_AUDIO_PERMISSION);
  }

  @Override
  public void onClick(View v) {
    if (v.getId() == R.id.start_recording) {
      Log.e(getClass().toString(), "starting recording");
      startVoiceRecorder();
    }
  }

  private static class ViewHolder extends RecyclerView.ViewHolder {

    TextView text;

    ViewHolder(LayoutInflater inflater, ViewGroup parent) {
      super(inflater.inflate(R.layout.item_result, parent, false));
      text = (TextView) itemView.findViewById(R.id.text);
    }

  }

  private static class ResultAdapter extends RecyclerView.Adapter<ViewHolder> {

    private final ArrayList<String> mResults = new ArrayList<>();

    ResultAdapter(ArrayList<String> results) {
      if (results != null) {
        mResults.addAll(results);
      }
    }

    @Override
    public ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
      return new ViewHolder(LayoutInflater.from(parent.getContext()), parent);
    }

    @Override
    public void onBindViewHolder(ViewHolder holder, int position) {
      holder.text.setText(mResults.get(position));
    }

    @Override
    public int getItemCount() {
      return mResults.size();
    }

    void addResult(String result) {
      mResults.add(0, result);
      notifyItemInserted(0);
    }

    public ArrayList<String> getResults() {
      return mResults;
    }

  }

}

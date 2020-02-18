package com.example.meelight;

import android.os.Bundle;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.snackbar.Snackbar;
import com.google.gson.Gson;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;

import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Button;
import android.widget.SeekBar;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class MainActivity extends AppCompatActivity {
    // POST for light update
    public StringRequest lightPost(boolean toggle, int brightness) {
        // Spits out a StringRequest for addition to the queue
        final String toggleString = toggle?"true":"false"; // God damn that's ugly
        final String brightnessString = Integer.toString(brightness); // BrightnessSsssSssString is snek var
        String url = "http://10.0.2.2:5000/api"; // TODO: placeholder
        StringRequest request = new StringRequest(Request.Method.POST, url, new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {
                Toast.makeText(MainActivity.this, response, Toast.LENGTH_SHORT).show();
                return;
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Toast.makeText(MainActivity.this, error.toString(), Toast.LENGTH_SHORT).show();
                return;
            }
        }) {
            @Override
            protected Map<String, String> getParams() {
                Map<String, String> params = new HashMap<>();
                params.put("toggle", toggleString);
                params.put("brightness", brightnessString);
                return params;
            }

            @Override
            public Map<String, String> getHeaders() throws AuthFailureError {
                Map<String, String> params = new HashMap<String, String>();
                params.put("Content-Type", "application/x-www-form-urlencoded");
                return params;
            }
        };
        return request;
    }
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        SeekBar brightBar = findViewById(R.id.brightBar);

        final TextView lightStatusText = findViewById(R.id.lightStatus);
        final JSONObject reqData;
        final Bulb bedroom = new Bulb();
        // Send a GET request to the server. Hardcoding for now
        final RequestQueue queue = Volley.newRequestQueue(this);
        //String url = "http://192.168.1.106:5000/api"; // TODO: Obvs a placeholder
        // Fun fact, the below is to access the emulating (host) machine
        String url = "http://10.0.2.2:5000/api"; // TODO: Obvs a placeholder

        brightBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {

            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                bedroom.setBrightness(seekBar.getProgress());
                queue.add(lightPost(false, bedroom.getBrightness()));

            }
        });
        final StringRequest statusRequest = new StringRequest(Request.Method.GET, url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        // Set status values here
                        //Toast.makeText(MainActivity.this, response, Toast.LENGTH_SHORT).show();
                        try {
                            JSONObject j = new JSONObject(response);
                            bedroom.setData(j);
                            if (bedroom.getPower()) {
                                lightStatusText.setText("ON");
                            }
                            else {
                                lightStatusText.setText("OFF");
                            }
                        }
                        catch (JSONException j) {
                            Toast.makeText(MainActivity.this, j.getMessage(), Toast.LENGTH_SHORT).show();
                        }
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Toast.makeText(MainActivity.this, error.getMessage(), Toast.LENGTH_SHORT).show();
            }
    });

        // POST for light manipulation


        // View controls
        Button refresh_b = findViewById(R.id.refresh_button);
        refresh_b.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                queue.add(statusRequest);
            }
        });
        Button toggle_b = findViewById(R.id.toggleButton);
        toggle_b.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                queue.add(lightPost(true, bedroom.getBrightness()));
            }
        });
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @Override
    protected void onDestroy() {

        super.onDestroy();
    }
}

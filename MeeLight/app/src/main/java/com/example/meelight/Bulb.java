package com.example.meelight;

import org.json.JSONException;
import org.json.JSONObject;

public class Bulb {
    private boolean power;
    private int brightness;
    private int[] rgb;

    public Bulb() {
        power = false;
        brightness = 100;
    }
    public Bulb(JSONObject bulbData) {
        // Constructor
        setData(bulbData);
    }
    public void setData(JSONObject bulbData) {
        try {
            String p = (String) bulbData.get("power");
            power = p.equals("on") ? true:false;
            brightness = Integer.parseInt((String) bulbData.get("bright"));
        }
        catch(JSONException ex) {
            // com.example.meelight.Bulb is almost certainly off if the JSON is empty
            power = false;
        }
    }
    public void setBrightness(int b) {
        if (b>-1 && b<101) {
            brightness = b;
        }
    }
    public boolean getPower() {
        return power;
    }
    public int getBrightness() {
        return brightness;
    }
    public int[] getRgb() {
        return rgb;
    }
}

package com.example.protectedfishing;

import android.accessibilityservice.AccessibilityService;
import android.content.Intent;
import android.net.Uri;
import android.provider.Browser;
import android.util.Log;
import android.view.accessibility.AccessibilityEvent;
import android.view.accessibility.AccessibilityNodeInfo;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class MyAccessibilityService extends AccessibilityService {

    static final private String TAG = "MyAccessibilityService";
    static final private Map<String, String> viewIdDict = new HashMap<String, String>()
    {{
        put("alook.browser", "search_fragment_input_view");
        put("alook.browser.google", "search_fragment_input_view");
        put("app.vanadium.browser", "url_bar");
        put("com.amazon.cloud9", "url");
        put("com.android.browser", "url");
        put("com.android.chrome", "url_bar");
        put("com.avast.android.secure.browser", "editor");
        put("com.avg.android.secure.browser", "editor");
        put("com.brave.browser", "url_bar");
        put("com.brave.browser_beta", "url_bar");
        put("com.brave.browser_default", "url_bar");
        put("com.brave.browser_dev", "url_bar");
        put("com.brave.browser_nightly", "url_bar");
        put("com.chrome.beta", "url_bar");
        put("com.chrome.canary", "url_bar");
        put("com.chrome.dev", "url_bar");
        put("com.cookiegames.smartcookie", "search");
        put("com.cookiejarapps.android.smartcookieweb", "mozac_browser_toolbar_url_view");
        put("com.duckduckgo.mobile.android", "omnibarTextInput");
        put("com.ecosia.android", "url_bar");
        put("com.google.android.apps.chrome", "url_bar");
        put("com.google.android.apps.chrome_dev", "url_bar");
        put("com.iode.firefox", "mozac_browser_toolbar_url_view");
        put("com.jamal2367.styx", "search");
        put("com.kiwibrowser.browser", "url_bar");
        put("com.kiwibrowser.browser.dev", "url_bar");
        put("com.microsoft.emmx", "url_bar");
        put("com.microsoft.emmx.beta", "url_bar");
        put("com.microsoft.emmx.canary", "url_bar");
        put("com.microsoft.emmx.dev", "url_bar");
        put("com.mmbox.browser", "search_box");
        put("com.mmbox.xbrowser", "search_box");
        put("com.mycompany.app.soulbrowser", "edit_text");
        put("com.naver.whale", "url_bar");
        put("com.neeva.app", "full_url_text_view");
        put("com.opera.browser", "url_field");
        put("com.opera.browser.beta", "url_field");
        put("com.opera.gx", "addressbarEdit");
        put("com.opera.mini.native", "url_field");
        put("com.opera.mini.native.beta", "url_field");
        put("com.opera.touch", "addressbarEdit");
        put("com.qflair.browserq", "url");
        put("com.qwant.liberty", "mozac_browser_toolbar_url_view,url_bar_title");
        put("com.rainsee.create", "search_box");
        put("com.sec.android.app.sbrowser", "location_bar_edit_text");
        put("com.sec.android.app.sbrowser.beta", "location_bar_edit_text");
        put("com.stoutner.privacybrowser.free", "url_edittext");
        put("com.stoutner.privacybrowser.standard", "url_edittext");
        put("com.vivaldi.browser", "url_bar");
        put("com.vivaldi.browser.snapshot", "url_bar");
        put("com.vivaldi.browser.sopranos", "url_bar");
        put("com.yandex.browser", "bro_omnibar_address_title_text,bro_omnibox_collapsed_title");
        put("com.yjllq.internet", "search_box");
        put("com.yjllq.kito", "search_box");
        put("com.yujian.ResideMenuDemo", "search_box");
        put("com.z28j.feel", "g2");
        put("idm.internet.download.manager", "search");
        put("idm.internet.download.manager.adm.lite", "search");
        put("idm.internet.download.manager.plus", "search");
        put("io.github.forkmaintainers.iceraven", "mozac_browser_toolbar_url_view");
        put("mark.via", "am,an");
        put("mark.via.gp", "as");
        put("net.dezor.browser", "url_bar");
        put("net.slions.fulguris.full.download", "search");
        put("net.slions.fulguris.full.download.debug", "search");
        put("net.slions.fulguris.full.playstore", "search");
        put("net.slions.fulguris.full.playstore.debug", "search");
        put("org.adblockplus.browser", "url_bar,url_bar_title");
        put("org.adblockplus.browser.beta", "url_bar,url_bar_title");
        put("org.bromite.bromite", "url_bar");
        put("org.bromite.chromium", "url_bar");
        put("org.chromium.chrome", "url_bar");
        put("org.codeaurora.swe.browser", "url_bar");
        put("org.gnu.icecat", "url_bar_title,mozac_browser_toolbar_url_view");
        put("org.mozilla.fenix", "mozac_browser_toolbar_url_view");
        put("org.mozilla.fenix.nightly", "mozac_browser_toolbar_url_view");
        put("org.mozilla.fennec_aurora", "mozac_browser_toolbar_url_view,url_bar_title");
        put("org.mozilla.fennec_fdroid", "mozac_browser_toolbar_url_view,url_bar_title");
        put("org.mozilla.firefox", "mozac_browser_toolbar_url_view,url_bar_title");
        put("org.mozilla.firefox_beta", "mozac_browser_toolbar_url_view,url_bar_title");
        put("org.mozilla.focus", "mozac_browser_toolbar_url_view,display_url");
        put("org.mozilla.focus.beta", "mozac_browser_toolbar_url_view,display_url");
        put("org.mozilla.focus.nightly", "mozac_browser_toolbar_url_view,display_url");
        put("org.mozilla.klar", "mozac_browser_toolbar_url_view,display_url");
        put("org.mozilla.reference.browser", "mozac_browser_toolbar_url_view");
        put("org.mozilla.rocket", "display_url");
        put("org.torproject.torbrowser", "mozac_browser_toolbar_url_view,url_bar_title");
        put("org.torproject.torbrowser_alpha", "mozac_browser_toolbar_url_view,url_bar_title");
        put("org.ungoogled.chromium.extensions.stable", "url_bar");
        put("org.ungoogled.chromium.stable", "url_bar");
        put("us.spotco.fennec_dos", "mozac_browser_toolbar_url_view,url_bar_title");
        put("acr.browser.barebones", "search");
        put("acr.browser.lightning", "search");
        put("com.feedback.browser.wjbrowser", "addressbar_url");
        put("com.ghostery.android.ghostery", "search_field");
        put("com.htc.sense.browser", "title");
        put("com.jerky.browser2", "enterUrl");
        put("com.ksmobile.cb", "address_bar_edit_text");
        put("com.lemurbrowser.exts","url_bar");
        put("com.linkbubble.playstore", "url_text");
        put("com.mx.browser", "address_editor_with_progress");
        put("com.mx.browser.tablet", "address_editor_with_progress");
        put("com.nubelacorp.javelin", "enterUrl");
        put("jp.co.fenrir.android.sleipnir", "url_text");
        put("jp.co.fenrir.android.sleipnir_black", "url_text");
        put("jp.co.fenrir.android.sleipnir_test", "url_text");
        put("mobi.mgeek.TunnyPair<String, String>", "title");
        put("org.iron.srware", "url_bar");
    }};

    private AccessibilityNodeInfo findUrlBar(AccessibilityNodeInfo node) {
        AccessibilityNodeInfo result;

        if (node.getClassName().toString().equals("android.widget.EditText")) {
            return node;
        }

        if (node.getChildCount() > 0) {
            for (int i = 0; i < node.getChildCount(); i++) {
                result = findUrlBar(node.getChild(i));
                if (result != null) {
                    return result;
                }
            }
        }

        return null;
    }

    private String getMaybeUrl(AccessibilityNodeInfo node) {
        AccessibilityNodeInfo urlBar;
        String packageName = node.getPackageName().toString();

        if (viewIdDict.containsKey(packageName)) {
            Log.d(TAG, "getMaybeUrl: Browser in viewid map");
            urlBar = node.findAccessibilityNodeInfosByViewId(packageName + ":id/" + viewIdDict.get(packageName)).get(0);
        }
        else {
            Log.d(TAG, "getMaybeUrl: Browser not in viewid map. Searching all children");
            urlBar = findUrlBar(node);  // not the best solution but ok
        }

        if (urlBar != null && urlBar.getClassName().toString().equals("android.widget.EditText")) {
            Log.d(TAG, "getMaybeUrl: Allegedly found urlBar " + urlBar);
            return urlBar.getText().toString();
        }

        return "";
    }

    @Override
    public void onAccessibilityEvent(AccessibilityEvent accessibilityEvent) {
        AccessibilityNodeInfo node = accessibilityEvent.getSource();
        String url = getMaybeUrl(node);

        if (url.length() == 0) {
            Log.d(TAG, "onAccessibilityEvent: Didn't find url");
        }
        else {
            Log.d(TAG, "onAccessibilityEvent: Found url " + url);

            JSONObject jsonRequestData = new JSONObject();
            try {
                jsonRequestData.put("url", url);
            } catch (JSONException e) {
                Log.d(TAG, "onAccessibilityEvent: JSONException " + e);
            }
            String requestData = jsonRequestData.toString();

            Log.d(TAG, "onAccessibilityEvent: Trying to send data " + requestData);

            ExecutorService mExecutor = Executors.newSingleThreadExecutor();
            Runnable backgroundRunnable = () -> {
                try {
                    Log.d(TAG, "onAccessibilityEvent: Connecting to server");
                    URL serverUrl = new URL("https://protected-fishing.vercel.app/check-url");
                    HttpURLConnection urlConnection = (HttpURLConnection) serverUrl.openConnection();
                    urlConnection.setRequestMethod("POST");
                    urlConnection.setDoOutput(true);
                    urlConnection.setRequestProperty("Content-Type", "application/json");
                    urlConnection.connect();

                    Log.d(TAG, "onAccessibilityEvent: Sending request");
                    OutputStream out = new BufferedOutputStream(urlConnection.getOutputStream());
                    BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(out, StandardCharsets.UTF_8));
                    writer.write(requestData);
                    writer.flush();
                    writer.close();
                    out.close();

                    Log.d(TAG, "onAccessibilityEvent: Reading response");
                    BufferedReader br;
                    int code = urlConnection.getResponseCode();
                    Log.d(TAG, "onAccessibilityEvent: Response code is " + code);
                    if (code == 200) {
                        br = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
                    } else {
                        br = new BufferedReader(new InputStreamReader(urlConnection.getErrorStream()));
                    }

                    String response = br.readLine(); // need to read response better
                    br.close();
                    Log.d(TAG, "onAccessibilityEvent: Response is " + response);
                } catch (Exception e) {
                    Log.d(TAG, "onAccessibilityEvent: Exception on server request " + e);
                }
            };

            mExecutor.execute(backgroundRunnable);

            Log.d(TAG, "onAccessibilityEvent: Opening another url");
            Intent intent = new Intent(Intent.ACTION_VIEW, Uri.parse("https://www.openu.ac.il/"));
            intent.setPackage("com.android.chrome");
            intent.putExtra(Browser.EXTRA_APPLICATION_ID, "com.android.chrome");
            intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_CLEAR_TASK | Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_SINGLE_TOP);
            startActivity(intent);
        }
    }

    @Override
    public void onInterrupt() {
    }
}

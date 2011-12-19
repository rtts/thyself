package nl.thyself.view;

import nl.thyself.R;
import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;
import android.widget.ArrayAdapter;
import android.widget.ListView;

public class MainActivity extends Activity {
  static final String[] QUESTIONS = new String[] {
    "I ate something sweet", 
    "I went outside", 
    "I started working"
  };
  
  int[] counter = new int[QUESTIONS.length];
  
  @Override
  public void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.main);
    ListView lv = (ListView) findViewById(R.id.list);
    lv.setAdapter(new ArrayAdapter<String>(this, R.layout.list_item, QUESTIONS));

    lv.setOnItemClickListener(new OnItemClickListener() {
      public void onItemClick(AdapterView<?> parent, View view,
          int position, long id) {
        // When clicked, increment counter and close activity
        counter[position]++;
        finish();
      }
    });
  }
  
  public void managePressed(View v) {
    // show counters
  }
}

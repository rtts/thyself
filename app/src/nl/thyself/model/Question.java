package nl.thyself.model;

public class Question {
  private long pk;
  private long serialId;
  private String text;
  private long time;
  
  public Question(long serialId, String text, long time) {
    this.setSerialId(serialId);
    this.setText(text);
    this.setTime(time);
  }
  
  public Question(long serialId, String text) {
    this(serialId, text, System.currentTimeMillis());
  }

  public long getSerialId() {
    return serialId;
  }

  public void setSerialId(long serialId) {
    this.serialId = serialId;
  }

  public String getText() {
    return text;
  }

  public void setText(String text) {
    this.text = text;
  }

  public long getTime() {
    return time;
  }

  public void setTime(long time) {
    this.time = time;
  }
  
}

package nl.thyself.model;

public class Answer {
  private long pk;
  private Question question;
  private long date;
  
  public Answer(Question question, long date) {
    this.setQuestion(question);
    this.setDate(date);
  }
  
  public Answer(Question question) {
    this(question, System.currentTimeMillis());
  }

  public Question getQuestion() {
    return question;
  }

  public void setQuestion(Question question) {
    this.question = question;
  }

  public long getDate() {
    return date;
  }

  public void setDate(long date) {
    this.date = date;
  }
}

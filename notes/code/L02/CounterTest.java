// java -cp /usr/share/java/junit4.jar:. \
//   org.junit.runner.JUnitCore CounterTest
import static org.junit.Assert.*;
import org.junit.Test;

public class CounterTest {
  @org.junit.Test
  public void add10() {
      Counter c = new Counter(); // arrange
      c.addToCount(10); // act
      // after calling SUT, read off results
      int count = c.getCount();
      assertEquals(10, count); // assert
  }
}

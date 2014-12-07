package Menu;

import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.Scanner;
/*******************************************************************************
 * This class is designed to allow functionality for text based games.
 * This class effectively redirects the input and output streams.
 *
 * @author seat3542
 *
 */
public class StreamGobbler extends Thread
{
	
	InputStream input;
	String nextLine = new String();
	boolean bThreadIsPaused = false;
	
	public StreamGobbler(InputStream input)
	{
		this.input = input; 
	}
	

	public void run()
	{
		 InputStreamReader reader = new InputStreamReader(input);
         @SuppressWarnings("resource")
		Scanner scan = new Scanner(reader);
         bThreadIsPaused = false;

         while (scan.hasNextLine()) 
         {
         	nextLine = scan.nextLine();
         	System.out.println(nextLine);
         }
         
         bThreadIsPaused = true;
	}
	
	public String getNextLine()
	{
		return nextLine;
	}
	
	public boolean getbIsPaused()
	{
		return bThreadIsPaused;
	}
}

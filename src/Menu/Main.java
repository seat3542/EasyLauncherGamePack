package Menu;
/*******************************************************************************
 * This class runs the menu
 * @author seat3542
 *
 */
public class Main 
{
	   public static void main (String args[])
	    {
		   GUI gui = new GUI();
	        javax.swing.SwingUtilities.invokeLater(new Runnable(){
	            @Override
				public void run()
	            {
	                gui.run();
	            }
	        });
	       
	    }
}
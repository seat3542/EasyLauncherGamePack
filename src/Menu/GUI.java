package Menu;

import java.awt.Dimension;
import java.awt.GridLayout;

import javax.swing.JFrame;
import javax.swing.JScrollPane;
import javax.swing.ScrollPaneConstants;
/*******************************************************************************
 * this class is responsible for creating the GUI for the menu
 * @author seat3542
 *
 */
public class GUI 
{
    public void run()
    {
    	   JFrame frame = new JFrame(Menu.GAME_TITLE);
           
           frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
           frame.setPreferredSize(new Dimension(Menu.FRAME_WIDTH,
        		   Menu.FRAME_HEIGHT));
          
           Menu theMenu = new Menu();
           theMenu.setLayout(new GridLayout(theMenu.getmSize(),1,1,10));
           theMenu.setOpaque(true);
          
           JScrollPane scroll = new JScrollPane(theMenu,
        		   ScrollPaneConstants.VERTICAL_SCROLLBAR_AS_NEEDED,
        		   ScrollPaneConstants.HORIZONTAL_SCROLLBAR_NEVER);
           frame.add(scroll);
          
           theMenu.createGameButtons();
          
           frame.pack();
           frame.setVisible(true);
    }
}

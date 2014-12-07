package Menu;

import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Scanner;

import javax.swing.JButton;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
/*******************************************************************************
 * This class is responsible for creating the easy game launcher Menu
 * @author seat3542
 *
 */
@SuppressWarnings("serial")
public class Menu extends JPanel implements ActionListener
{
    private Tuple mButtonNames[];
    private int mSize = -1;
    private JButton mButtons[];
    private final static String FILE = "Buttons.txt";
    public final static String GAME_TITLE = "Easy Game Launcher";
    private final static String CURRENT_DIR = "user.dir";
    private final static String DIR_PATH = "/Games/";
    private final static String TITLE = "About";
    private final static String FOLDER_NAME = "/TextFiles/";
    public final static int FRAME_WIDTH = 400;
    public final static int FRAME_HEIGHT = 600;
    public final static int BUTTON_HEIGHT = 100;
    public final static int BUTTON_WIDTH= 400;
    private String mContent;
   
   
    public Menu ()
    {
        this.getArraySize();
        this.fillButtonArray();
    }
    /***************************************************************************
     * This function gets the size of mButtonNames array by reading from 
     * Buttons.txt and determining how many
     * games there are.
     */
    private void getArraySize()
    {
        try
        {
            BufferedReader reader = new BufferedReader(new FileReader (FILE));
            while (reader.readLine() != null)
            {
                mSize ++;
            }
           
            this.mButtonNames = new Tuple[mSize];
            reader.close();
        }
        catch(IOException e)
        {
            e.printStackTrace();
        }
       
    }
    /***************************************************************************
     * this function fills the mButtonNames array with all necessary 
     * information
     */
    private void fillButtonArray()
    {
        try
        {
            Scanner scanner = new Scanner (new File(FILE));
            scanner.useDelimiter(";");
            scanner.nextLine(); // throw away first line since it's an example
           
            for (int i = 0; i < mSize; i++)
            {
                this.mButtonNames[i] = new Tuple(scanner.next(),scanner.next(),
                		scanner.next(),scanner.next());
            }
           
            scanner.close();
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
       
    }
    /***************************************************************************
     * this button dynamically creates game buttons based off of the number of 
     * games in the Buttons.txt file
     */
    public void createGameButtons()
    {
        mButtons = new JButton[mSize];
       
        for (int i = 0; i < mSize; i++)
        {
            JButton temp= new JButton(mButtonNames[i].getGameTitle());
            temp.addActionListener(this);
            temp.setPreferredSize(new Dimension(BUTTON_WIDTH,BUTTON_HEIGHT));
            add(temp);
            mButtons[i] = temp;   
        }
    }
    /***************************************************************************
     * this function looks for a button press. Upon a button press, the user is
     *  prompted with an optionDialog giving relevant about information and 
     *  an option to play the game
     *
     */
    @Override
    public void actionPerformed(ActionEvent e)
    {
        String temp = e.getActionCommand();
        int whichIndex = -1; // negative number indicates no index found
       
        for (int i = 0; i < mSize; i ++)
        {
            if (mButtonNames[i].getGameTitle() == temp)
            {
                whichIndex = i;
                break;
            }
        }
       
        temp = concatPath (mButtonNames[whichIndex]);
        try
        {
            aboutAction(temp,mButtonNames[whichIndex].getExecutable(),
            		mButtonNames[whichIndex].getAbout());
        }
        catch (FileNotFoundException e1)
        {
            // TODO Auto-generated catch block
            e1.printStackTrace();
        }
    }
    /***************************************************************************
     * this function creates a process based on which button was selected. 
     * Essentially this function launches the game you select
     * @param dirPath - directory path relevant to your machine
     * @param executable - name of executable
     */
    private void createProcess(String dirPath,String executable)
    {
        String workingDir = System.getProperty(CURRENT_DIR);
        if (!testExec(workingDir + dirPath + "/" + executable))
        {
            changePermissions(workingDir + dirPath + "/" + executable);
        }
        ProcessBuilder pb = new ProcessBuilder(workingDir + dirPath + "/" + 
        executable);
        try
        {
            pb.directory(new File(workingDir + dirPath));
            pb.start();
        }
        catch (IOException e)
        {
            e.printStackTrace();
        }
    }
    /***************************************************************************
     * Concatenates DIR_PATH which is a string containing the folder name of 
     * where the games are located in front of the folder name of the game 
     * selected
     * @param buttonName
     * @return - returns string of concatenated path
     */
    private String concatPath(Tuple buttonName)
    {
        return DIR_PATH + buttonName.getFolderName();
    }
    /***************************************************************************
     * this function tests if the game is executable
     * @param executable - name of executable
     * @return - true if the game has permissions to be executed, otherwise 
     * false
     */
    private boolean testExec(String executable)
    {
        return (new File(executable).canExecute());
    }
    /***************************************************************************
     * This function changes the permissions of an executable to true
     * @param executable - name of executable
     */
    private void changePermissions(String executable)
    {
        new File(executable).setExecutable(true);
    }
    /***************************************************************************
     * this function displays an optionDialog that allows the user to get about
     * information pertaining to the game. Furthermore, this function has a play
     * option that when pressed launches the game.
     *
     * @param dirPath - path to the game
     * @param executable = name of game executable
     * @param whichFile - name of file to be looked for
     * @throws FileNotFoundException - exception if file name is not found
     */
    public void aboutAction(String dirPath,String executable,String whichFile) 
    		throws FileNotFoundException
    {
        Object[] options = {"Play"};
        this.createAboutText(whichFile);
        int reply = JOptionPane.showOptionDialog(null,mContent,TITLE,
        		JOptionPane.YES_OPTION,JOptionPane.QUESTION_MESSAGE,null,
        		options,options[0]);
        if (reply == JOptionPane.YES_OPTION)
        {
            createProcess(dirPath,executable);
        }       
    }
    /**************************************************************************
     * this function reads from a file all about information and records it 
     * into a single string.
     * @param whichFile - the file to read from
     * @throws FileNotFoundException - exception if file is not found
     */
    @SuppressWarnings("resource")
    public void createAboutText(String whichFile) throws FileNotFoundException
    {
        String fileName = System.getProperty(CURRENT_DIR) + FOLDER_NAME + 
        		whichFile;
        this.mContent = new Scanner(new File(fileName)).useDelimiter("\\Z")
        		.next();
    }
    public int getmSize()
    {
    	return this.mSize;
    }
}
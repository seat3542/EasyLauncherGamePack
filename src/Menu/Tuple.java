package Menu;
/********************************
 * Data structure created to easily hold strings.
 * @author seat3542
 *
 */
public class Tuple
{
    String mExecutable;
    String mGameTitle;
    String mFolderName;
    String mAbout;
   
    public Tuple(String gameTitle,String folderName,String executable,
    		String about)
    {
        this.mExecutable = executable;
        this.mGameTitle = gameTitle;
        this.mFolderName = folderName;
        this.mAbout = about;
    }
   
    public String getExecutable()
    {
        return this.mExecutable;
    }
   
    public String getGameTitle()
    {
        return this.mGameTitle;
    }
   
    public void setGameTitle(String gameTitle)
    {
        this.mGameTitle = gameTitle;
    }
    public void setExecutable(String executable)
    {
        this.mExecutable = executable;
    }
    public String getFolderName()
    {
        return this.mFolderName;
    }
    public String getAbout()
    {
    	return this.mAbout;
    }
   
}

To run the test:
Add the extension Katalon Recorder (Selenium IDE for Chrome) in Google Chrome. (Link: chrome://extensions/?id=ljdobmomdgdljniojadhoplhkpialdid)
Download the Chrome Web Driver and unzip if required. (Link: vhttp://chromedriver.chromium.org/downloads)
In Start Menu, search for Environment Variables and click on Edit the system environment variables 
Click on Environment Variables... 
In System variables panel, select Path variable and click on Edit.
Click on New and add file path to the chrome driver. Do not include the file name in the file path.
It is recommended that the system be restarted or else the tests might fail.
Click on the Katalon Recorder to bring up the Katalon Recorder window.
Click on the Folder icon to add a test suite. Navigate to OPSTestCases test suite and double-click on it.
After the test suite is loaded, click on UploadLessonPlanTest test case and change the value of file path to where your file is located.
Click on Play Suite button to run all the test cases in the test suite.
Note: The test cases were built when the server was running in port 8080.
# THIS SOFTWARE IS PROVIDED BY MURATA "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# MURATA BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# Python 3.x

##################################################################
import urllib.request
import urllib.error
import base64
import msvcrt # Windows only!
import time
username = 'admin' # Username to access HTTP API
password = 'admin' # Password to access HTTP API
ip = input('Insert IP address: ') # IP of the BSN
ip = 'http://' + ip
# HTTP Basic authentication
headers = {'Authorization': 'Basic ' + base64.b64encode((username + ':' + password).encode('utf-8')).decode()}

#############################################################
def sendMessage(path,body):
    # Sends HTTP GET/POST to predefined IP
    #try:
    request = urllib.request.Request(ip+path, body, headers)
    result = urllib.request.urlopen(request)
    
    #print(result.code)
    #print(result.info())
    
    response = result.read().decode('utf-8')
    # except urllib.error.URLError:
    # response = 'Connection timed out.'
    return response
 
 
 
def calibrationMenu():
    print('CALIBRATION MENU\n\
    \'1\'\tCalibration info\n\
    \'2\'\tEmpty bed calibration\n\
    \'3\'\tOccupied bed calibration\n\
    \'esc\'\tExit calibration menu\n')
    while 1:
    
        keypress = msvcrt.getch()
        if keypress == chr(27).encode():
            break
    
        elif keypress == str('1').encode():
            # 4.12 Query BCG Calibration Status
            response = sendMessage('/bcg/cali',None)
            print(response)
            
        elif keypress == str('2').encode():
            # 4.13 Start BCG Calibration (phase 1 = empty bed)
            response = sendMessage('/bcg/cali','{"phase": 1}'.encode('utf-8'))
            print(response)
            if response == '{"errno": 0}':
                print('Starting empty bed calibration. (60s)')
                print(str(0), end=" ", flush=True) # flush forces write
                for i in range(1,7):
                    time.sleep(10)
                    print(str(i*10), end=" ", flush=True )
                    print('\nEmpty bed calibration finished')
            else:
                print('Empty bed calibration start failed')
                print(response) # Read the HTTP API for response definitions
        elif keypress == str('3').encode():
            # 4.13 Start BCG Calibration (phase 2 = occupied bed)
            response = sendMessage('/bcg/cali','{"phase": 2}'.encode('utf-8'))
            print(response)
            if response == '{"errno": 0}':
                print('Starting occupied bed calibration. (60s)')
                print(str(0), end=" ", flush=True)
                for i in range(1,7):
                    time.sleep(10)
                    print(str(i*10), end=" ", flush=True )
                    print('\nOccupied bed calibration finished')
            else:
                print('Occupied calibration start failed')
                print(response) # Read the HTTP API for response definitions
            
            
def main():
    # Main Menu
    while 1:
       print('\nBCG HTTP API main menu\n\
       \'1\'\tBCG info\n\
       \'2\'\tCalibration menu\n\
       \'esc\'\tQuit program\n')
       keypress = msvcrt.getch()
       if keypress == chr(27).encode():
           break
       elif keypress == str('1').encode():
           # 4.2 Query Basic BCG Info
           response = sendMessage('/bcg',None)
           print(response) # Read the HTTP API for response definitions
       elif keypress == str('2').encode():
           calibrationMenu()

if __name__ == '__main__':
 main()
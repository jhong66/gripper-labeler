import cv2, argparse, os, csv, pickle

cwd = os.getcwd()

parser = argparse.ArgumentParser()
parser.add_argument('--path', type=str, default="frames")
parser.add_argument('--filename', type=str, default="frame")
parser.add_argument('-c', '--counter', type=int, default=1)

args = parser.parse_args()

fields = ['img', 'x1', 'y1', 'x2', 'y2']

# function to display the coordinates of
# of the points clicked on the image
def onClick(event, x, y, flags, params):
  global Running
  global Clickcount
  global Coords
  global Imgname

  # checking for left mouse clicks
  if event == cv2.EVENT_LBUTTONDOWN:
    print(x, ' ', y)
    Coords.append((x,y))

    rad = 2
    img[y-rad:y+rad, x-rad:x+rad] = [0,0,255]
    Clickcount += 1
    if Clickcount == 2:
      newrow = {'img': Imgname,
                'x1': Coords[0][0], 
                'y1': Coords[0][1],
                'x2': Coords[1][0],
                'y2': Coords[1][1]}
      with open("trajlabels.csv", "a", newline='') as file:
        writer = csv.DictWriter(file, fieldnames = fields) 
        writer.writerow(newrow)

      Running = False
      Clickcount = 0
    print(Running)
    print(Clickcount)

# driver function
if __name__=="__main__":
  imgdir = cwd + "\\" + args.path
  filenamepattern = args.filename

  counter = args.counter
  imgpath = imgdir + "\\" + filenamepattern + str(counter).zfill(4) + ".pickle"
  print(imgpath)
  Imgname = filenamepattern + str(counter).zfill(4) + ".pickle"

  while os.path.exists(imgpath):
    with open(imgpath, 'rb') as handle:
        frame_data = pickle.load(handle)
        img = frame_data['rgb']
    print(img.shape)

    wname = Imgname
    cv2.namedWindow(winname=wname)
    cv2.setMouseCallback(wname, onClick)
    
    # # img resizing - probably comment out
    # scale_percent = 50 # percent of original size
    # width = int(img.shape[1] * scale_percent / 100)
    # height = int(img.shape[0] * scale_percent / 100)
    # dim = (width, height)
    # img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    Running = True
    Clickcount = 0
    Coords = []
    while Running:
      cv2.imshow(wname, img)
      cv2.waitKey(1)

    cv2.destroyAllWindows()

    counter += 1
    imgpath = imgdir + "\\" + filenamepattern + str(counter).zfill(4) + ".pickle"
    Imgname = filenamepattern + str(counter).zfill(4) + ".pickle"
    print(imgpath)
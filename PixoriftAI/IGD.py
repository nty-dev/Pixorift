from google_images_download import google_images_download as gid

keywordlist = []
chromedriver_path = 'C:\Program Files\chromedriver\chromedriver.exe'

print('Welcome to the Image Data Generator.')
print('This programme helps you obtain free image data for any project!')

no = input('Please enter the number of images you wish to obtain for each keyword: ')
print('To end the keyword chain, enter "Done".')

o = True
while o:
    r = input('Please input keyword: ')
    if r.lower() == 'done':
        o = False
    elif ',' in r:
        print('Commas not allowed!')
    elif r == '':
        print('Blanks not allowed!')
    else:
        keywordlist.append(r)
    
for i in keywordlist:
    gidinit = gid.googleimagesdownload()
    infodict = {'keywords': i, 'limit': no, 'print_urls': True, 'output_directory': './ImageDB', 'chromedriver': chromedriver_path}
    imagepath = gidinit.download(infodict)
    print(imagepath)

input('Press ENTER to exit...')

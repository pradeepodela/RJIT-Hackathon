
from branch1 import *
from branch2 import *
from branch3 import *
import cv2
import requests
from tracker import *
from datetime import datetime
import streamlit as st
import tempfile
import time 
from send import senddata
# Create tracker object
tracker = EuclideanDistTracker()



source = 1 
vechicles = {}
global save_video
save_video = True # want to save video? (when video as source)
show_video=True # set true when using video file
save_img=True  # set true when using only image file to save the image
tracker_status = True
confidence = 0.7
emg_detector = False
accused_detection = True
object_det = True
helemet_detecation = False
Start = True

Email = 'odelapradeep12@gmail.com'
# when using image as input, lower the threshold value of image classification

#saveing video as output
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, frame_size)
amc = 0
fir = 0
pol = 0








###################################################################################################
########################################### UI PART ###############################################
###################################################################################################



st.title('Dashboard ')
st.sidebar.title('settings')

st.markdown(
	'''
	<style>
	[data-testid='sidebar'][aria-expanded='true'] > div:firstchild{width:400px}
	[data-testid='sidebar'][aria-expanded='false'] > div:firstchild{width:400px , margin-left: -400px}
	</style>
	''',
	unsafe_allow_html=True
)

st.sidebar.markdown('---')

save_video = st.sidebar.checkbox('save video',value=True)
show_video = st.sidebar.checkbox('show video',value=True)
save_img = st.sidebar.checkbox('save image',value=True)
st.sidebar.markdown('---')
st.sidebar.title("Video source")

use_webcam = st.sidebar.checkbox('use webcam',value=False)
if use_webcam:
	cams = [0,1,3]
	source = st.sidebar.multiselect('choose a cam' , cams , default=1)
	listToStr = ' '.join([str(elem) for elem in source])
	in_source = int(listToStr)
	if len(source) > 1:
		st.sidebar.text('plese select only one')
	if len(source) == 0:
		st.sidebar.text('plese select a camara')
	source = int(source[0])
	print(source)
	
else:
	source = st.sidebar.file_uploader('upload a video ' , type=['mp4','mov','avi','m4v','gif'])
	show = st.sidebar.checkbox('show input video ' , value=False)
	if show:
		st.sidebar.video(source)
	if source != None:
		tfile = tempfile.NamedTemporaryFile(delete=False) 
		tfile.write(source.read())
		in_source = tfile.name
st.sidebar.markdown('---')
st.sidebar.title("functionality's")

emg_detector = st.sidebar.checkbox('Emergency vechicle detecation',value=True)
accused_detection = st.sidebar.checkbox('Accused detection detecation',value=True)
helemet_detecation = st.sidebar.checkbox('Helemet detection ',value=True)
# object_det = st.sidebar.checkbox('object detection and tracking',value=True)
# if object_det:
# 	confidence = st.sidebar.slider('confidence',min_value=0.0,max_value=1.0,value=0.7)
	



# st.sidebar.markdown('---')
# st.sidebar.title("Email")
# email_check = st.sidebar.checkbox('Use custom Email ',value=True)
# if email_check:
# 	Email_in = st.sidebar.text_input('please enter the email')
# 	st.sidebar.text(Email_in)
st.sidebar.markdown('---')

# if len(Email_in ) > 1:
# 	print('gr888')
# 	send_email = Email_in
# else:
# 	send_email = Email





Start = st.sidebar.button('Start')

stop = st.sidebar.button('Stop')
if stop: 
	Start = False
	print(Start)
    





###################################################################################################
########################################### UI PART ###############################################
###################################################################################################





























if Start:

	stframe = st.empty()

	cap = cv2.VideoCapture(in_source)
	while(cap.isOpened()):
		ret, frame = cap.read()


		




		if emg_detector:
			tex1 , ambulance , firengine = emergency_vechicledetecation(frame)

			print(amc)
			


			if ambulance == 'ambulance:1.0':
				amc = amc+1

			if firengine == 'firengine:1.0':
				fir = fir+1

			

			if amc == 10 :
				print('emergency vechicle found ambulance')
				try:
					print('sending api request to the traffic signal...')
					requests.get('http://188.166.206.43/Xhi9PCKQtq0deTV0zM9OxuRVcHSu5aMR/update/V1?value=1')
					print('success traffic light changed')
					amc = 0
				except: print('error sending the data')
				print(tex1)



		now = datetime.now()
		dtstr = now.strftime('%H:%M')
		time_now = dtstr.replace(':','.')
		
		
		
		
		
		if ret == True:
			
			
			frame = cv2.resize(frame, frame_size)  # resizing image
			orifinal_frame = frame.copy()

			if accused_detection:  
				from app import *
				img = fcr(frame)

				# frame = atn(frame,send_email)




			if helemet_detecation:
				# print('helemet detecation started')
			
				frame, results = object_detection(frame) 
				

				rider_list = []
				head_list = []
				number_list = []

				for result in results:
					x1,y1,x2,y2,cnf, clas = result
					if clas == 0:
						rider_list.append(result)
					elif clas == 1:
						head_list.append(result)
					elif clas == 2:
						number_list.append(result)

				for rdr in rider_list:
					time_stamp = str(time.time())
					
					x1r, y1r, x2r, y2r, cnfr, clasr = rdr
					for hd in head_list:
						x1h, y1h, x2h, y2h, cnfh, clash = hd
						if inside_box([x1r,y1r,x2r,y2r], [x1h,y1h,x2h,y2h]): # if this head inside this rider bbox
							try:
								head_img = orifinal_frame[y1h:y2h, x1h:x2h]
								helmet_present = img_classify(head_img)
							except:
								helmet_present[0] = None

							if  helmet_present[0] == True: # if helmet present
								frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0,255,0), 1)
								frame = cv2.putText(frame, f'{round(helmet_present[1],1)}', (x1h, y1h+40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)

								
							elif helmet_present[0] == None: # Poor prediction
								frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0, 255, 255), 1)
								frame = cv2.putText(frame, f'{round(helmet_present[1],1)}', (x1h, y1h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)


							elif helmet_present[0] == False: # if helmet absent 
								frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0, 0, 255), 1)
								frame = cv2.putText(frame, f'{round(helmet_present[1],1)}', (x1h, y1h+40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
								if 1 == 1:
									
									
									cv2.imwrite(f'riders_pictures/{time_now}.png', frame[y1r:y2r, x1r:x2r])
									email_img = frame[y1r:y2r, x1r:x2r]
									print('sending mail........')
									email_img = cv2.imencode('.png',email_img)
									print('video encoded')
									#Wtime.sleep(0.5)
									data = f'Accused Found!!\n\n-------------------------------\nVoliation: Helemet not waring\n\nFound at: University Rajasthan College\nLocation: https://www.google.com/maps?q=17.5368066,78.3844026&z=17&hl=en \n-------------------------------'

									senddata(f'riders_pictures/{time_now}.png',data)
									# email_me(f'riders_pictures/{time_now}.png',send_email,time_now)
									
									print('mail is sent....')
								else:
									print('could not save rider')
								eml_path = str(f'riders_pictures/{time_now}.png')
								

								for num in number_list:
									x1_num, y1_num, x2_num, y2_num, conf_num, clas_num = num
									if inside_box([x1r,y1r,x2r,y2r], [x1_num, y1_num, x2_num, y2_num]):
										try:
											num_img = orifinal_frame[y1_num:y2_num, x1_num:x2_num]
											cv2.imwrite(f'number_plates/{time_now}.jpg', num_img)
											text = get_text(f'number_plates/{time_now}.jpg')
											if text:
												print(text)
											else: print('text not found')
										except:
											print('could not save number plate')
			# if object_det:
			# 	frame , objects = img_p(frame,tracker_plt=tracker_status,thres=confidence)
			# 	print(objects)
										
			if save_video: # save video
				out.write(frame)
			if save_img: #save img
				cv2.imwrite('saved_frame.jpg', frame)
			if show_video: # show video
				frame = cv2.resize(frame, (900, 450))  # resizing to fit in screen
				if emg_detector:cv2.putText(frame,tex1,(15,20),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),2)
				frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
				stframe.image(frame)
				#cv2.imshow('Frame', frame)


			if cv2.waitKey(1) & 0xFF == ord('q'):
				cap.release()
				cv2.destroyAllWindows()
				print('Execution completed')
				break


		else:
			break

	cap.release()
	cv2.destroyAllWindows()
print('Execution completed')


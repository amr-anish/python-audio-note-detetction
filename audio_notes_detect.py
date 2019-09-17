import numpy as np
import wave
import struct
import math
#Teams can add other helper functions
#which can be added here
#amr c0der ----------------------------------------------Copyright----------------------------------------------amr c0der

split=[]
sampling_freq = 44100	# Sampling frequency of audio signal
win_size=882            # Window Size is 882 frames

def rms(sound,count,win_size):           #Function to calculate the rms Value
    sum=0
    for j in range(count,count+win_size):
            sum=sum+(sound[j]*sound[j])
    sum=sum/win_size
    result=math.sqrt(sum)
    
    return result

def f_equ(sound,start,end):              #Function to calculate Frequency
    start1=start*win_size
    end1=(end+1)*win_size
    split=sound[start1:end1] 
    ftransform=np.fft.fft(split)
    ft=np.argsort(ftransform)
    rev=ft[::-1]
    l=(end-start+1)*win_size
    f=(rev[0]*sampling_freq)/l
    if(f>10000):
        f=44100-f
    return f


def matching_freq(freq):                #Function to match Frequency to corresponding notes
    note=[]
    for i in range(len(freq)):
        if(freq[i]<1046):
            note.append('C6')
        elif(freq[i]>1110 and freq[i]<1246):
            note.append('D6')
        elif(freq[i]>1246 and freq[i]<1357.5):
            note.append('E6')
        elif(freq[i]>1357.5 and freq[i]<1482.5):
            note.append('F6')
        elif(freq[i]>1482.5 and freq[i]<1664):
            note.append('G6')
        elif(freq[i]>1664 and freq[i]<1867.5):
            note.append('A6')
        elif(freq[i]>1867 and freq[i]<2034):
            note.append('B6')
        elif(freq[i]>2034 and freq[i]<2221):
            note.append('C7')
        elif(freq[i]>2221 and freq[i]<2493):
            note.append('D7')
        elif(freq[i]>2493 and freq[i]<2715.5):
            note.append('E7')
        elif(freq[i]>2715.5 and freq[i]<2967):
            note.append('F7')
        elif(freq[i]>2967 and freq[i]<3328):
            note.append('G7')
        elif(freq[i]>3328 and freq[i]<3735.5):
            note.append('A7')
        elif(freq[i]>3735.5 and freq[i]<4086.5):
            note.append('B7')
        elif(freq[i]>4086.5 and freq[i]<4442):
            note.append('C8')
        elif(freq[i]>4442 and freq[i]<4986):
            note.append('D8')
        elif(freq[i]>4986 and freq[i]<5430.5):
            note.append('E8')
        elif(freq[i]>5430 and freq[i]<5929):
            note.append('F8')
        elif(freq[i]>5929 and freq[i]<6655.5):
            note.append('G8')
        elif(freq[i]>6655.5 and freq[i]<7471):
            note.append('A8')
        elif(freq[i]>7471 and freq[i]<8000):
            note.append('B8')
    return note


def play(sound_file):
    file_length=sound_file.getnframes()      
    sound= np.zeros(file_length)        
    for i in range(file_length):
        data = sound_file.readframes(1)
        data= struct.unpack("<h",data)
        sound[i]=int(data[0])
    sound= np.divide(sound, float(2**15))

    #Detecting silence
    
    T_hld=0.0319366455078125                # Threshold value 
    re=np.zeros(file_length/win_size)       # Array to store the result of silence
    for i in range(file_length/win_size):
        count=i*win_size
        Rms=rms(sound,count,win_size) 
        if(Rms<T_hld):
            re[i]=0
        else:
            re[i]=1
            
    #Detecting location of notes
            
    ST=0               # Start point of frame
    freq=[]            # List to store frequencies
    f_ct=0             # Index for frequency list
    FL=re[0]           # Flag registere for detecting location
    for i in range(file_length/win_size):
        if(re[i]!=FL):
            FL=re[i]
            end=i-1
            if(re[i-1]==1):
                freq.append(f_equ(sound,ST,end))
                f_ct=f_ct+1
                ST=end+1
            else:
                ST=end+1
                
    Identified_Notes=matching_freq(freq)
    return Identified_Notes

############################## Read Audio File #############################

if __name__ == "__main__":
    #code for checking output for single audio file
    #sound_file = wave.open('Audio_files/Audio_2.wav', 'r')
    #Identified_Notes = play(sound_file)
    #print "Notes = ", Identified_Notes

    #code for checking output for all images
    Identified_Notes_list = []
    for file_number in range(1,6):
        file_name = "Audio_files/Audio_"+str(file_number)+".wav"      #specif file path here
        sound_file = wave.open(file_name)
        Identified_Notes = play(sound_file)
        Identified_Notes_list.append(Identified_Notes)
        print Identified_Notes

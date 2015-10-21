from kzpy import *
from kzpy.img import ProgressBar

def load_and_format_frames_to_5Hz_April2015(relevant_video_frame_files):
    # - load 25Hz & 5Hz videos
    # do not run this by mistake
    for e in relevant_video_frame_files:
        print('*** ' + e)
        for t in relevant_video_frame_files[e]:
            print('\t' + e)
            r = relevant_video_frame_files[e][t]
            print('*** Loading ' + r['path'])
            mat = scipy.io.loadmat(r['path'])
            if r['25Hz_frames']:
                print('25Hz_frames to 5Hz frames ' + e + t)
                r['25Hz_frames'] = mat[r['mat_key']]
                print(np.shape(relevant_video_frame_files[e][t]['25Hz_frames']))
                r['5Hz_frames'] = LOCAL_FUNCTION_get_5Hz_frames_from_25Hz_frames(r['25Hz_frames'])
                print(np.shape(relevant_video_frame_files[e][t]['5Hz_frames']))
            else:
                r['5Hz_frames'] = mat[r['mat_key']]
                print('5Hz_frames ' + e + t)
                print(np.shape(relevant_video_frame_files[e][t]['5Hz_frames']))
            
            

def LOCAL_FUNCTION_get_5Hz_frames_from_25Hz_frames(frames_25Hz):
    n_frames = np.shape(frames_25Hz)[0]
    W = np.shape(frames_25Hz)[1]

    frames_5Hz = np.zeros((n_frames/5,W,W))
    pb = ProgressBar(W)
    for x in range(W):
        pb.animate(x+1)
        for y in range(W):
            frames_5Hz[:,x,y] = (frames_25Hz[:,x,y]).reshape(-1,5).mean(axis=1)
    return frames_5Hz
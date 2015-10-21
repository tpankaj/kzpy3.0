from kzpy3.vis import *


"""vis stands for Visualize. These are functions to look at fMRI data."""

def horizontal(vol,z_start,rows,columns,fig=1):
    #pylab.rcParams['figure.figsize'] = big_figure_size
    """Show a brain in horizontal slices"""
    r,c = rows,columns
    num_slices = r * c
    for z in range(z_start,z_start+num_slices):
        mi(vol[:, :, z],fig,[r,c,z-z_start+1],z)

def coronal(vol,z_start,rows,columns,fig=2):
    #pylab.rcParams['figure.figsize'] = big_figure_size
    """Show a brain in horizontal slices"""
    r,c = rows,columns
    num_slices = r * c
    for z in range(z_start,z_start+num_slices):
        mi(np.rot90(vol[:,z,:]),fig,[r,c,z-z_start+1],z)

def sagital(vol,z_start,rows,columns,fig=3):
    #pylab.rcParams['figure.figsize'] = big_figure_size
    """Show a brain in horizontal slices"""
    r,c = rows,columns
    num_slices = r * c
    for z in range(z_start,z_start+num_slices):
        mi(np.rot90(vol[z,:,:]),fig,[r,c,z-z_start+1],z)


def volume(vol,z_start,rows,columns):
    horizontal(vol,z_start,rows,columns)


        
        
        
def timecourses(data,subject,x,y,z,relevant_experiments):
    s = subject
    pylab.rcParams['figure.figsize'] = (30,30)
    ctr = 0
    for e in relevant_experiments:
        for t in relevant_experiments[e]:
            ctr += 1
            f = plt.figure(1)
            f.add_subplot(6,1,ctr)
            a = data[e][t][s]['all_run_avg'][x,y,z,:]-data[e][t][s]['all_run_avg'][x,y,z,:].mean()
            b = data[e][t][s]['odd_run_avg'][x,y,z,:]-data[e][t][s]['odd_run_avg'][x,y,z,:].mean()
            c = data[e][t][s]['even_run_avg'][x,y,z,:]-data[e][t][s]['even_run_avg'][x,y,z,:].mean()
            plt.plot(a,label='all')
            plt.plot(b,label='odd')
            plt.plot(c,label='even')
            plt.legend()
            plt.title(e + ': ' + t + ' r=' + str(np.corrcoef(b,c)[0,1]))
            
def concatenated_timecourses(data,subject,x,y,z,relevant_experiments):
    s = subject
    alls,evens,odds = kzpy.fMRI.data.get_concatenated_alls_evens_odds(data,relevant_experiments,s,x,y,z,0)
    pylab.rcParams['figure.figsize'] = (30,7)
    f = plt.figure(1)
    f.add_subplot(2,1,1)
    plt.plot(evens,'g-',label='evens')
    plt.plot(odds,'b-',label='odds')
    plt.xlim(0,len(evens))
    plt.title((x,y,z))
    f.add_subplot(2,6,7)
    plt.plot(evens,odds,'.')
    plt.title(np.corrcoef(evens,odds)[0,1])
    #plt.xlim(-1500,1500)
    #plt.ylim(-1500,1500)
    #plt.axes().set_aspect('equal', 'datalim')

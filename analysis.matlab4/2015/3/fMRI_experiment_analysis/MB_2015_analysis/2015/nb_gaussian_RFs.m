%%%%%%%%%%% Standard Notebook Beginning %%%%%%%%%%%%
%
clc; fprintf('%s\n',[mfilename ' (' mfilename('fullpath') '.m)']);
this_filename = mfilename('fullpath');
this_file_text = fileread([this_filename,'.m']);
if not(exist('G'))
    error('NOTE: run local_startup.m manually at the beginning of the Matlab session.');
end
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
GRAPHICS = 1;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Description . . .
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 10;
    sd=40;%img_wid/2^5;
    img_wid = 512+2*16;
    img = square_single_zeros(img_wid);
    img_blank = img;
    
    g=gaussian_matrix2(6*sd,sd);
    
    mi(img);
    ctr=0;
    for x = (-img_wid/2+3*sd+1):(2*sd):(img_wid/2-3*sd+1)
        for y = (-img_wid/2+3*sd+1):(2*sd):(img_wid/2-3*sd+1)
            ctr=ctr+1;
            if randn(1)>0
                img_blank = 0*img_blank;
                img = img + place_img_A_in_img_B(g,img_blank,x,y);
                mi(img,1);drawnow;
            end
        end
    end
    ctr
end
if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
    h = 0*(1:10000);
    for i = 1:10000
        h(i) = model_HRF(i/1000);
    end
    s = 0*(1:448);
    t=0*(1:(300*1000));
    for i = 0:1:47
        i
        t(6000+(i*6000):(6000+i*6000+4000)) = 1;
    end
    c=conv(t,h,'same');
    c=c-mean(c);c=c/std(c);
    f=real(abs(fft(c)));
    mp({c,'.-'},9,[2,1,1]);
    mp({f,'o-'},9,[2,1,2]);axis([0,100,0,max(f)]);

end

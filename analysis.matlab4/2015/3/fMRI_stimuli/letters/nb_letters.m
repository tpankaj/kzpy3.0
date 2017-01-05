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
CELL_NUM = 1;
    abc = containers.Map;

    upper_letter_strs = {'A','B','C','D','E','F','G','H','I','J',...
        'K','L','M','N','O','P','Q','R','S','T',...
        'U','V','W','X','Y','Z','period','question_mark'};
    for i = 1:length(upper_letter_strs)
        img = imread(['~/Desktop/letters/upper/',upper_letter_strs{i},'.png']);
        img = zeroToOneRange(squeeze(img(:,:,1)));
        abc(upper_letter_strs{i}) = img;
    end
    lower_letter_strs = {'a' 'b' 'c' 'd' };
    for i = 1:length(lower_letter_strs)
        img = imread(['~/Desktop/letters/lower/',lower_letter_strs{i},'.png']);
        img = zeroToOneRange(squeeze(img(:,:,1)));
        abc(lower_letter_strs{i}) = img;
    end
    abc(' ') = 0*img;
    abc('.') = abc('period');
    abc('?') = abc('question_mark');
end
if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
    txt = 'THE dOG aTE THE cAT. SHE SaId TO HaRRY dO YOU WaNT TO FIGHT THE dRaGON? HE SaId NO. BUT THEN HE WENT aNYWaY BEcaUSE IT WaS FUN. CaN YOU PaY aTTENTION TO THE FacES WHEN YOU aRE REaDING THE LETTERS? MOST PEOPLE THINK IT IS dIFFIcULT. SO dO I.';
    img = zeros(200,200);%+0.5;img(1,1)=1;img(1,2)=0;
    ctr = 4;
    tic
    
video_name = 'reading_10Feb2015';
mkdir(d2s({'~/Desktop/' video_name '.' now}));
outputVideo = VideoWriter(d2s({'~/Desktop/' video_name '.' now '/' video_name '.' now '.avi'}),'Uncompressed AVI');%'Motion JPEG AVI');%
outputVideo.FrameRate = 5;
open(outputVideo);

    for i = 1:length(txt)
        for j = 1:2
            ctr = ctr + 1;
            if ctr == 20
                toc
                nat_img = zeroToOneRange( sqsing(stimTrn512_int8(randi(1750),:,:)));
                ctr = 0;
            end
            if j == 1
                %character = abc(letter_strs{randi(28)});%abc(txt(i));
                character = abc(txt(i));
            else
                character = 0* character;
            end
            img2 = place_img_A_in_img_B(...
                reduceMatrixByHalf(...
                reduceMatrixByHalf(...
                reduceMatrixByHalf(...
                place_img_A_in_img_B(character,img,0,0)))),nat_img,0,0);
            mi( img2);
            writeVideo(outputVideo,img2);
            pause(1/5);
    %         mi(img);
    %         pause(1/5);
        end
    end
    close(outputVideo);

end

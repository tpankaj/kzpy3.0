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
% Make the video for the Vermeer attending and reading experiment used with S1_2015 in February and March, 2015. Tested this script 23 March, 2015.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
    abc = containers.Map;

    upper_letter_strs = {'A','B','C','D','E','F','G','H','I','J',...
        'K','L','M','N','O','P','Q','R','S','T',...
        'U','V','W','X','Y','Z','period','question_mark','exclamation','double_quote','single_quote', 'comma' };
    for i = 1:length(upper_letter_strs)
        img = imread(['~/Data/stimuli/2015/2/text/letters/upper/',upper_letter_strs{i},'.png']);
        img = zeroToOneRange(squeeze(img(:,:,1)));
        abc(upper_letter_strs{i}) = img;
    end
    lower_letter_strs = {'a' 'b' 'c' 'd' 'e' 'f' 'g' 'h' 'i' 'j' 'k' 'l' 'm' 'n' 'o' 'p' 'q' 'r' 's' 't' 'u' 'v' 'w' 'x' 'y' 'z'};
    for i = 1:length(lower_letter_strs)
        img = imread(['~/Data/stimuli/2015/2/text/letters/lower/',lower_letter_strs{i},'.png']);
        img = zeroToOneRange(squeeze(img(:,:,1)));
        abc(lower_letter_strs{i}) = img;
    end
    abc(' ') = 0*img;
    abc('.') = abc('period');
    abc('?') = abc('question_mark');
    abc('!') = abc('exclamation');
    abc('"') = abc('double_quote');
    abc('''') = abc('single_quote');
    abc(',') = abc('comma');
    character = 0 * abc('a');
end
if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
    txt = fileread('alternateIthacaTom_wdh_corr.txt');%text;%'THE dOG aTE THE cAT. SHE SaId TO HaRRY dO YOU WaNT TO FIGHT THE dRaGON? HE SaId NO. BUT THEN HE WENT aNYWaY BEcaUSE IT WaS FUN. CaN YOU PaY aTTENTION TO THE FacES WHEN YOU aRE REaDING THE LETTERS? MOST PEOPLE THINK IT IS dIFFIcULT. SO dO I.';
    img = zeros(200,200,3);%+0.5;img(1,1)=1;img(1,2)=0;
    ctr = 4;
    tic
    
video_name = 'reading_10Feb2015';
mkdir(d2s({'~/Desktop/' video_name '.' now}));
outputVideo = VideoWriter(d2s({'~/Desktop/' video_name '.' now '/' video_name '.' now '.avi'}),'Uncompressed AVI');%'Motion JPEG AVI');%
outputVideo.FrameRate = 5;
open(outputVideo);
v = zeros(6,384,512,3,'single');
blank = zeros(384,512,3,'single')+0.5;
blank_fix = blank;
blank_fix(190:194,254:258,:)=0;
for p = 1:6
    v(p,:,:,:) = imread(d2s({'~/Desktop/Artists/Vermeer_512/Vermeer_' p '.jpg'}));
end
for i = 1:5*6
    mi( blank_fix);
    writeVideo(outputVideo,blank_fix);
    pause(1/50);
end
task = 1;
txt_ctr = 1;
nat_img = v(1);
for the_block = 1:8
    for p = 1:6
        for i = 1:6*5
            if mod(i,2)==0
                if task == 1
                    character = abc('x');%abc(txt(randi(length(txt))));
                else
                        character = abc(txt(txt_ctr));
                        txt_ctr = txt_ctr+1;
                        if txt_ctr > length(txt)
                            txt_ctr = 1;
                        end
                end
            else
                character = 0* character;
            end
 
            nat_img = squeeze(v(p,:,:,:));
            nat_img = single(nat_img);
            nat_img = nat_img / max(max(max(nat_img)));
            if i < 4*5
                display_image = nat_img;
            else
                display_image = blank;
            end
            c_size = size(character);
            character = zeroToOneRange(character);
            if p == 6
                if i == 27
                    task = task + 1;
                    if task > 2
                        task = 1;
                    end
                end
            end
            character_RGB = zeros(c_size(1),c_size(2),3,'single');
            character_RGB(:,:,1)=zeroToOneRange( character);
            character_RGB(:,:,2)=zeroToOneRange( character);
            character_RGB(:,:,3)=zeroToOneRange( character);
            if task == 2
                character_RGB(:,:,2) = 0.5*character_RGB(:,:,2);
                character_RGB(:,:,3) = 0.5*character_RGB(:,:,3);
            end

            mini_text = imresize(place_img_A_in_img_B(character_RGB,img,0,0),1/6);
            mini_text = (mini_text-min(min(min(mini_text))));
            mini_text = mini_text/ max(max(max(mini_text)));
            img2 = place_img_A_in_img_B(mini_text,display_image,0,0);
            mi( img2);
            writeVideo(outputVideo,img2);
            pause(1/500);

        end
    end
end
for i = 1:5*6
    mi( blank_fix);
    writeVideo(outputVideo,blank_fix);
    pause(1/50);
end
close(outputVideo);

end

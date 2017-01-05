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

% xy_offsets = zeros(6,2,2);
%     for p=1:6
%         for task = 1:2
%             nat_img = squeeze(v(p,:,:,:));
%             nat_img = single(nat_img);
%             nat_img = nat_img / max(max(max(nat_img)));
%             mi(nat_img,1)
%             [x,y] = ginput(1)
%             xy_offsets(p,task,:) = round([x y]);
%         end
%     end
% return

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
WRITE_VIDEO = true;
if WRITE_VIDEO
    video_name = 'reading_10Feb2015';
    mkdir(d2s({'~/Desktop/' video_name '.' now}));
    outputVideo = VideoWriter(d2s({'~/Desktop/' video_name '.' now '/' video_name '.' now '.avi'}),'Motion JPEG AVI');%'Uncompressed AVI');%
    outputVideo.FrameRate = 5;
    outputVideo.Quality = 99;
    open(outputVideo);
end
v = zeros(6,384,512,3,'single');
blank = zeros(384,512,3,'single')+0.5;
blank_fix = blank;
blank_fix(190:194,254:258,:)=0;
for p = 1:6
    v(p,:,:,:) = imread(d2s({'~/Data/stimuli/2015/2/11Feb2015_Vermeer_reading_videos/Vermeer_512/Vermeer_' p '.jpg'}));
end
for i = 1:5*6
    mi( blank_fix);
    if WRITE_VIDEO
        writeVideo(outputVideo,blank_fix);
    end
    pause(1/50);
end
task = 1;
txt_ctr = 1;
x_offset = round(200*rand(6,2)-100);
y_offset = round(200*rand(6,2)-100);
NATURAL_IMAGE = 1;
NO_IMAGE = 0;
nat_img = v(1);
paintings = [2 3 4];
for the_block = 1:8
    for p = paintings
        [x_offset(p,task) y_offset(p,task)]
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
            if and(i > 2*5, i <= 3*5)
                moment = NATURAL_IMAGE;
                display_image = nat_img;
            else
                moment = NO_IMAGE;

                display_image = blank;
            end
            c_size = size(character);
            character = zeroToOneRange(character);
            if p == max(paintings)
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

            % mini_text = imresize(place_img_A_in_img_B(character_RGB,img,0,0),1/6);
            % mini_text = (mini_text-min(min(min(mini_text))));
            % mini_text = mini_text/ max(max(max(mini_text)));
            mini_text = zeros(6,6,3);
            mini_text(3:4,3:4,:) = 1.0;
            if task == 1
                mini_text(:,:,2:3) = 0;
            else
                mini_text(:,:,[1 3]) = 0;
            end
            if moment == NATURAL_IMAGE
                img2 = place_img_A_in_img_B(mini_text,display_image,0,0);
            else
                if i > 1*5
                    
                    img2 = place_img_A_in_img_B(mini_text,display_image, 0, 0);
                else
                    
                    img2 = place_img_A_in_img_B(mini_text,display_image, 0, 0);
                end
            end
            mi( img2);
            if WRITE_VIDEO
                writeVideo(outputVideo,img2);
            end
            drawnow;%pause(1/5);

        end
    end
end
for i = 1:5*6
    mi( blank_fix);
    if WRITE_VIDEO
        writeVideo(outputVideo,blank_fix);
    end
    pause(1/50);
end
if WRITE_VIDEO
    close(outputVideo);
end

end

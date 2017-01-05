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
        video_name = 'vermeer_TMS_9April2015';
        mkdir(d2s({'~/Desktop/' video_name '.' now}));
        outputVideo = VideoWriter(d2s({'~/Desktop/' video_name '.' now '/' video_name '.' now '.avi'}),'Motion JPEG AVI');%'Uncompressed AVI');%
        outputVideo.FrameRate = 10;
        outputVideo.Quality = 99;
        open(outputVideo);
    end
    fixspot_TRs = textread('/Users/davidzipser/Google_Drive/Data/stimuli/2015/4/9April2015 TMS jittered design/fixspot.txt');
    picture_TRs = textread('/Users/davidzipser/Google_Drive/Data/stimuli/2015/4/9April2015 TMS jittered design/picture.txt');
    TMS_level_TRs = textread('/Users/davidzipser/Google_Drive/Data/stimuli/2015/4/9April2015 TMS jittered design/TMS_level.txt');
    fixspot_TRs = int8(round(2*zeroToOneRange(fixspot_TRs)));
    TMS_level_TRs = int8(round(TMS_level_TRs));
    picture_TRs = int8(round(picture_TRs));
    hold off;plot(fixspot_TRs,'g');hold on;plot(-picture_TRs,'r');plot(TMS_level_TRs,'b');hold off;
    v = zeros(6,384,512,3,'single');
    blank = zeros(384,512,3,'single')+0.5;
    blank_fix = blank;
    blank_fix(190:194,254:258,:)=0;
    for p = 1:6
        img = imread(d2s({'~/Data/stimuli/2015/2/11Feb2015_Vermeer_reading_videos/Vermeer_512/Vermeer_' p '.jpg'}));
        img = single(img);
        img = img / max(max(max(img)));
        v(p,:,:,:) = img;
        mi(v(p,:,:,:),1);
        pause(0.5)
    end

    for tr = 1:length(fixspot_TRs)
        tr
        fx = fixspot_TRs(tr);
        pc = picture_TRs(tr);
        tm = TMS_level_TRs(tr);

        mini_text = zeros(6,6,3);
        mini_text(3:4,3:4,:) = 1.0;
        if fx == 2
            mini_text(3:4,3:4,2) = 0.6;
            mini_text(3:4,3:4,3) = 0.4;
        elseif fx == 1
            mini_text(3:4,3:4,1) = 0.3;
            mini_text(3:4,3:4,2) = 0.7;
        end
        %mi(mini_text)
        if pc > 0
            display_image = squeeze(v(pc+1,:,:,:));
        else
            display_image = blank;
        end
        f = place_img_A_in_img_B(mini_text,display_image, 0, 0);
        for i = 1:9
            mi(f);
            if WRITE_VIDEO
                writeVideo(outputVideo,f);
            end
            pause(1/100);
        end
    end
    if WRITE_VIDEO
        close(outputVideo);
    end
end

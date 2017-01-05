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


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 11 January 2015.
% 12 Jan.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
GRAPHICS = 1;
if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CELL_NUM = 1;
    N=100000;
    d1 = randn(N,1)*10+10;
    d2 = randn(N/10,1)*20+40;
    d3 = randn(N/100,1)*(-20)-30;
    d = [d1;d2;d3];
    z1 = z_score(d);
    z2 = z_score_aggressive(d);
    
    if GRAPHICS
        fsp(1,[2,2,1]);
        hist(d,100);
        fsp(1,[2,2,3]);
        hist(z1,100);title(median(z1));
        fsp(1,[2,2,4]);
        hist(z2,100);title(median(z2));
    end
end


if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CELL_NUM = 1;
    a = sqsing(get_Kay_image('Val',21));
    b = zeroToOneRange( sqsing(stimValHP_SD6(21,:,:)) ).^(1/4);
    c = 1-b;%sqsing(stimValHP_SD6(21,:,:));
    %ci = color_modulation_of_grayscale_image3(a,[],zeroToOneRange(b).^1,zeroToOneRange(c).^1,false);
    ci = color_modulation_of_grayscale_image3(a,[],zeroToOneRange(a).^1,[],true);
    mi(ci,1,[1,2,1]);
    mi(b,1,[1,2,2]);
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CELL_NUM = 1;
    a = sqsing(G.stimTrn512_int8(1,:,:));
    b = sqsing(G.stimTrn512_int8(17,:,:));
    c = sqsing(G.stimTrn512_int8(1469,:,:));
    ci = color_modulation_of_grayscale_image3(a,zeroToOneRange(b).^4,zeroToOneRange(c).^4,[],true);
    mi(ci,1,[1,2,1]);
end

if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    CELL_NUM = 2;
    a = sqsing(G.stimTrn512_int8(1,:,:));
    b = sqsing(G.stimTrn512_int8(17,:,:));
    c = sqsing(G.stimTrn512_int8(1469,:,:));
    d = sqsing(G.stimTrn512_int8(555,:,:));
    ci = color_modulation_of_grayscale_image3(a,zeroToOneRange(b).^1,zeroToOneRange(c).^1,zeroToOneRange(d).^1,true);
    mi(ci,1,[1,2,2]);
end

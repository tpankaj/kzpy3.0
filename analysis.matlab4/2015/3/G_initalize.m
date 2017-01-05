%function G_initalize
% G_initalize
% 12 December 2014, WHV

clc

fprintf('function G_initalize . . . \n');




if not(exist('LOCAL_STARTUP'))
    error('NOTE: run local_startup.m manually at the beginning of the Matlab session.');
end

clear G;

global G

G = [];
G.home = d2s({'/Users/' getenv('USER')});

if strcmp(G.home,'/Users/internetaccess')
    if length(dir('/Volumes/Karl Zipser fMRI2/External_Desktop')) > 0
        G.Desktop = '/Volumes/Karl Zipser fMRI2/External_Desktop'
    elseif length(dir('/Volumes/26Oct2014/External_Desktop')) > 0
        G.Desktop = '/Volumes/26Oct2014/External_Desktop'
    else
        my_pause('Warning: external drive/Portable_drive not found, using ~/Desktop, hit Return to continue.');
        
        G.Desktop = '~/Desktop';
    end
else
    G.Desktop = '~/Desktop';
end
G.Desktop


G.description = data2newlineStr({
    '_______________________________'
    'G is my global data structure.'
    'G.home is the user dir.'
    'G.description is this.'
    ''
    'G.e is an array of experiments.'
    'G.e().description describes the experiment'
    'G.e().v is an array of experiments versions.'
    'G.e().v.description'
    ''
    'G.e().v().s is an array of subjects.'
    ''
    'G.e().v().s().stim is an array of stim conditions.'
    'G.e().v().s().stim().description'
    'G.e().v().s().stim().data'
    ''
    'G.e().v().s().roi is a array of rois'
    'G.e().v().s().roi().indicies is a array of indicies'
    'G.e().v().s().roi().description describes the roi'
    ''
    'G.e().v().s().RFs, these two are contemplated . . .'
    'G.e().v().s().Pimages'
    ''
    'e.g., G.e(KAY_2008).v(NOV_2013_SINGLE_TRIAL).s(1).stim(TRN).description'
    ''
    'G.constants holds constants'
    ''
    '_______________________________'
    });

%%%%%%%%%%%%%%% Kay 2008 %%%%%%%%%%%%%%
G.constants.KAY_2008 = 1;
G.constants.NOV_2013_SINGLE_TRIAL = 1;
G.constants.NOV_2013_COMBINED_TRIALS = 2;
G.constants.TRN = 1;
G.constants.VAL = 2;
G.constants.V1 = 1;
G.constants.V2 = 2;
G.constants.V3 = 3;
G.constants.V4 = 6;
G.constants.V3a = 4;
G.constants.V3b = 5;
G.constants.LO = 7;
G.constants.OTHER = 0;
G.constants.GOOD = 9;
G.constants.V1V2 = 10;

KAY_2008 = G.constants.KAY_2008;
NOV_2013_SINGLE_TRIAL = G.constants.NOV_2013_SINGLE_TRIAL;
NOV_2013_COMBINED_TRIALS = G.constants.NOV_2013_COMBINED_TRIALS;
TRN = G.constants.TRN;
VAL = G.constants.VAL;
V1 = G.constants.V1;
V2 = G.constants.V2;
V3 = G.constants.V3;
V4 = G.constants.V4;
V3a = G.constants.V3a;
V3b = G.constants.V3b;
LO = G.constants.LO;
OTHER = G.constants.OTHER;
GOOD = G.constants.GOOD;
V1V2 = G.constants.V1V2;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%% MB analysis Feb 2015 %%%%%%%
% G.constants.Phantom = 100;
% G.constants.HVO = 101;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%





G.description
fprintf('G:\n');
G
fprintf('G.constants:\n');
G.constants

E = G.constants.KAY_2008;

G.e(E).description = 'Kendrick Kay 2008 natural image experiment';

if false
    fprintf('loading G.stimVal512_uint8 . . .\n');
    load([G.Desktop '/fMRI_top_node/data.fMRI/experiment-Kay_2008/stimuli-stimVal/version-512px/stimVal512_uint8.mat']);
    G.stimVal512_uint8 = stimVal512_uint8; clear stimVal512_uint8;
    fprintf('loading G.stimTrn512_int8 . . .\n');
    load([G.Desktop '/fMRI_top_node/data.fMRI/experiment-Kay_2008/stimuli-stimTrn/version-512px/stimTrn512_int8.mat']);
    G.stimTrn512_int8 = stimTrn512_int8; clear stimTrn512_int8;
end

G.temp.temp_image_file_counter = 0;

if false
    GD = [];
    GD.path_to_Kay_2008 = '~/Desktop/fMRI_top_node/data.fMRI/experiment-Kay_2008/';
    GD.path_to_sets_semantic = [GD.path_to_Kay_2008, 'stimuli-stimTrn/sets-semantic/'];
    GD.path_to_stimTrn_images = [GD.path_to_Kay_2008,'stimuli-stimTrn/version-512px/format-png/'];

    GD.semantic_sets_stimTrn = containers.Map;
    semantic_set_folders = dir([GD.path_to_sets_semantic, 'set-*']);
    for i = 1:length(semantic_set_folders)
        path_and_filename = [GD.path_to_sets_semantic, semantic_set_folders(i).name,'/'];
        GD.semantic_sets_stimTrn(semantic_set_folders(i).name) = get_set_of_indicies2_1(path_and_filename, 'png');
    end
    G.semantic_sets_stimTrn=GD.semantic_sets_stimTrn;
end

fprintf( 'Done.\n' )
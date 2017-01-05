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
GRAPHICS = false;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% dicom_preprocess_script
% 30 Jan. 2015
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if 1%%%%%% 20 June 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    subject = 'S1_2014';year=2015;month=6;day=21;
    %my_dicom_to_nii( subject, year, month, day, 'gre_field_mapping_16Mar2015_', [1]);
    my_dicom_to_nii( subject, year, month, day, 'mb_bold_mb6_20mm_AP_PSN_', [4 14]);
end
if 0%%%%%% 20 June 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    subject = 'S1_2014';year=2015;month=6;day=20;
    my_dicom_to_nii( subject, year, month, day, 'gre_field_mapping_16Mar2015_', [11 12 30 31]);
    my_dicom_to_nii( subject, year, month, day, 'mb_bold_mb6_20mm_AP_PSN_', [4 6 8 10 12 14 16 18 20 22 24 26 28 30 32 34 36 38 40 42 44 46 48 50 52 54 56 58 60 62 64 66 68 70 72 74 76]);
end
if 0%%%%%% 21 June 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    subject = 'S6_2015';year=2015;month=6;day=21;
    %my_dicom_to_nii( subject, year, month, day, 'gre_field_mapping_16Mar2015_', [17 18 43 44]);
    my_dicom_to_nii( subject, year, month, day, 'mb_bold_mb6_20mm_AP_PSN_', [38 40 42]);%[4 6 8 10 12 14 16 18 20 22 24 26 28 30 32 34 36 38 40 42]);
end
if 0%%%%%% 17 June 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    subject = 'S4_2015';year=2015;month=6;day=17;
    my_dicom_to_nii( subject, year, month, day, 'gre_field_mapping_16Mar2015_', [47 48]);
    my_dicom_to_nii( subject, year, month, day, 'mb_bold_mb6_20mm_AP_PSN_', [6 8 10 12 14 16 18 20 22 24 26 28 30 32 34 36 38 40 42 44 46]);
end
if 0%%%%%% 15 June 2015 (acutally 14 June afternoon session) %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    subject = 'HVO';year=2015;month=6;day=15;
    my_dicom_to_nii( subject, year, month, day, 'mb_bold_mb6_20mm_AP_PSN_', [6 8 10 12 14 16 18 20]);
end
if 0%%%%%% 14 June 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    subject = 'HVO';year=2015;month=6;day=14;
    my_dicom_to_nii( subject, year, month, day, 'mb_bold_mb6_20mm_AP_PSN_', [4 6 8 10 12 14 16 18 20]);
end
if 0%%%%%% 9 April 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    subject = 'S5_2015';year=2015;month=6;day=3;
    my_dicom_to_nii( subject, year, month, day, 'mb_bold_mb6_20mm_AP_PSN_', [4 6 8 10 12 14 16 18 20]);
end
if 0%%%%%% 9 April 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    subject = 'S5_2015';year=2015;month=4;day=9;
    my_dicom_to_nii( subject, year, month, day, 'gre_field_mapping_16Mar2015_', [21 22]);
    my_dicom_to_nii( subject, year, month, day, 'mb_bold_mb6_20mm_AP_PSN_', [4 6 8 10 12 14 16 18 20]);
end
if 0%%%%%% 16 April 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    subject = 'HVO';year=2015;month=4;day=16;
    my_dicom_to_nii( subject, year, month, day, 'gre_field_mapping_16Mar2015_', [13 14 29 30]);
    my_dicom_to_nii( subject, year, month, day, 'mb_bold_mb6_20mm_AP_PSN_', [8 10 12 20 22 24 26 28]);
end
if 0%%%%%% 7 April 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    subject = 'HVO';year=2015;month=4;day=7;
    my_dicom_to_nii( subject, year, month, day, 'gre_field_mapping_16Mar2015_', [9 10 19 20]);
    my_dicom_to_nii( subject, year, month, day, 'mb_bold_mb6_20mm_AP_PSN_', [4 6 8 14 16 18]);
end
if 0%%%%%% 3 April 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    subject = 'HVO';year=2015;month=4;day=3;
    my_dicom_to_nii( subject, year, month, day, 'gre_field_mapping_16Mar2015_', [23 24 37 38]);
    my_dicom_to_nii( subject, year, month, day, 'mb_bold_mb6_20mm_AP_PSN_', [16 18 20 22 30 32 34]);
end
if 0%%%%%% 2 April 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    my_dicom_to_nii( 'HVO', 2015, 4, 2, 'gre_field_mapping_16Mar2015_', [15 16]);
    my_dicom_to_nii( 'HVO', 2015, 4, 2, 'mb_bold_mb6_20mm_AP_PSN_', [6 8 10 12 14]);
end
if 0%%%%%% 30 Mar 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    my_dicom_to_nii( 'HVO', 2015, 3, 30, 'gre_field_mapping_16Mar2015_', [13 14 25 26]);
    my_dicom_to_nii( 'HVO', 2015, 3, 30, 'mb_bold_mb6_20mm_AP_PSN_', [4 6 10 12 18 20 22 24]);
end
if 0%%%%%% 29 Mar 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    my_dicom_to_nii( 'HVO', 2015, 3, 29, 'gre_field_mapping_16Mar2015_', [11 12 27 28]);
    my_dicom_to_nii( 'HVO', 2015, 3, 29, 'mb_bold_mb6_20mm_AP_PSN_', [4 6 8 10 16 20 22 26]);
end
if 0%%%%%% 27 Mar 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    my_dicom_to_nii( 'HVO', 2015, 3, 27, 'gre_field_mapping_16Mar2015_', [13 14 23 24]);
    my_dicom_to_nii( 'HVO', 2015, 3, 27, 'mb_bold_mb6_20mm_AP_PSN_', [4 6 8 10 16 18 20 22]);
end
if 0%%%%%% 26 Mar 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    my_dicom_to_nii( 'HVO', 2015, 3, 26, 'gre_field_mapping_16Mar2015_', [13 14 23 24]);
    my_dicom_to_nii( 'HVO', 2015, 3, 26, 'mb_bold_mb6_20mm_AP_PSN_', [4 6 8 10 12 18 20 22]);
end
if 0%%%%%% 24 Mar 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    my_dicom_to_nii( 'HVO', 2015, 3, 24, 'gre_field_mapping_16Mar2015_', [11 12 23 24]);
    my_dicom_to_nii( 'HVO', 2015, 3, 24, 'mb_bold_mb6_20mm_AP_PSN_', [4 6 8 10 16 18 20 22]);
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if 0%%%%%% 23 Mar 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    my_dicom_to_nii( 'HVO', 2015, 3, 23, 'gre_field_mapping_16Mar2015_', [11 12]);
    my_dicom_to_nii( 'HVO', 2015, 3, 23, 'mb_bold_mb6_20mm_AP_PSN_', [4 6 8 10]);
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if 0%%%%%% 22 Mar 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    my_dicom_to_nii( 'AA', 2015, 3, 22, 'gre_field_mapping_16Mar2015_', [17 18]);
    my_dicom_to_nii( 'AA', 2015, 3, 22, 'mb_bold_mb6_20mm_AP_PSN_', [4 6 8 10 12 14 16]);
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if 0%%%%%% 21 p.m. Mar 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    my_dicom_to_nii( 'HVO', 2015, 3, 21, 'gre_field_mapping_16Mar2015_', [11 12 23 24]);
    my_dicom_to_nii( 'HVO', 2015, 3, 21, 'mb_bold_mb6_20mm_AP_PSN_', [4 6 8 10 16 18 20 22]);
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if 0%%%%%% 19 p.m. Mar 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % Note, 20 actually means 19 p.m.
    my_dicom_to_nii( 'HVO', 2015, 3, 20, 'gre_field_mapping_16Mar2015_', [11 12 23 24]);
    my_dicom_to_nii( 'HVO', 2015, 3, 20, 'mb_bold_mb6_20mm_AP_PSN_', [4 6 8 10 16 18 20 22]);
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if 0%%%%%% 19 Mar 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    my_dicom_to_nii( 'HVO', 2015, 3, 19, 'gre_field_mapping_16Mar2015_', [11 12]);
    my_dicom_to_nii( 'HVO', 2015, 3, 19, 'mb_bold_mb6_20mm_AP_PSN_', [4 6 8 10]);
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if 0%%%%%% 18 Mar 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    my_dicom_to_nii( 'HVO', 2015, 3, 18, 'gre_field_mapping_16Mar2015_', [11 12]);
    my_dicom_to_nii( 'HVO', 2015, 3, 18, 'mb_bold_mb6_20mm_AP_PSN_', [4 6 8 10]);
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if 0%%%%%% 16 Mar 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    my_dicom_to_nii( 'HVO', 2015, 3, 16, 'gre_field_mapping_16Mar2015_', [11 12]);
    %my_dicom_to_nii( 'HVO', 2015, 3, 16, 'mb_bold_mb6_20mm_AP_PSN_', [4 6 8 10]);
    %my_dicom_to_nii( 'Phantom', 2015, 3, 13, 'mb_bold_mb6_20mm_AP_PSN_', [4]);
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if 0%%%%%% 14 Mar 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
    my_dicom_to_nii( 'HVO', 2015, 3, 14, 'gre_field_mapping_', [11 12]);
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if 0%%%%%% 14 Mar 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
    my_dicom_to_nii( 'HVO', 2015, 3, 14, 'mb_bold_mb6_20mm_AP_PSN_', [4 6 8 10]);
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if 0%%%%%% 12 Mar 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
    my_dicom_to_nii( 'AV', 2015, 3, 12, 'mb_bold_mb6_20mm_AP_PSN_', [4 6 8 12 14]);
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if 0%%%%%% 9 Mar 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
    my_dicom_to_nii( 'HVO', 2015, 3, 9, 'mb_bold_mb6_20mm_AP_PSN_', [6 8 10 12]);
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if 0%%%%%% 27 Feb 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
    my_dicom_to_nii( 'HVO', 2015, 2, 27, 'mb_bold_mb8_20mm_AP_PSN_', [4 6 8 10]);
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if 0 %%%%%% 26 Feb 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
    my_dicom_to_nii( 'HVO', 2015, 2, 26, 'mb_bold_mb8_20mm_AP_PSN_', [4 6 8 10]);
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if 0 %%%%%% 20 Feb 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
    my_dicom_to_nii( 'HVO', 2015, 2, '20Feb2015_Zipser_Pilots_HVO', 'mb_bold_mb8_20mm_AP_PSN_', [4 6 8]);
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if 0 %%%%%% 19 Feb 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
    my_dicom_to_nii( 'DR', 2015, 2, '19Feb2015_Zipser_Pilots_DR_testing_32ch_for_TMS_use', 'mb_bold_mb6_20mm_AP_PSN_', [4 6]);
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if 0 %%%%%% 18 Feb 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
    my_dicom_to_nii( 'HVO', 2015, 2, '18Feb2015_Zipser_Pilots_HVO', 'mb_bold_mb6_20mm_AP_PSN_', [4 6 8 10]);
    my_dicom_to_nii( 'HVO', 2015, 2, '18Feb2015_Zipser_Pilots_HVO', 'mb_bold_mb8_20mm_AP_PSN_', [12]);
    my_dicom_to_nii( 'Phantom', 2015, 2, '18Feb2015_Zipser_Pilots_Phantom', 'mb_bold_mb6_20mm_AP_PSN_', [8]);
    my_dicom_to_nii( 'Phantom', 2015, 2, '18Feb2015_Zipser_Pilots_Phantom', 'mb_bold_mb8_20mm_AP_PSN_', [6]);
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if 0 %%%%%% 16 Feb 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
    my_dicom_to_nii( 'HVO', 2015, 2, '16Feb2015_Zipser_Pilots_HVO', 'mb_bold_mb6_20mm_AP_PSN_', [5 9 11 13 19 21 25]);
    my_dicom_to_nii( 'Phantom', 2015, 2, '16Feb2015_Zipser_Pilots_Phantom', 'mb_bold_mb6_20mm_AP_PSN_', [4]);
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if 0 %%%%%% 14 Feb 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
    my_dicom_to_nii( 'HVO', 2015, 2, '14Feb2015_Zipser_Pilots_HVO', 'mb_bold_mb6_20mm_AP_PSN_', [6 8 10 12 14]);
    my_dicom_to_nii( 'HVO', 2015, 2, '14Feb2015_Zipser_Pilots_HVO', 'gre_field_mapping_', [3 4]);
    
    my_dicom_to_nii( 'Phantom', 2015, 2, '14Feb2015_Zipser_Pilots_Phantom', 'mb_bold_mb6_20mm_AP_PSN_', [8 10]);
    %my_dicom_to_nii( 'Phantom', 2015, 2, '14Feb2015_Zipser_Pilots_Phantom', 'gre_field_mapping_', [9 10]);
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if 0 %%%%%% 12 Feb 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
    my_dicom_to_nii( 'HVO', 2015, 2, '12Feb2015_Zipser_Pilots_HVO', 'mb_bold_mb6_20mm_AP_PSN_', [6 8 10]);
    my_dicom_to_nii( 'HVO', 2015, 2, '12Feb2015_Zipser_Pilots_HVO', 'gre_field_mapping_', [3 4]);
    
    my_dicom_to_nii( 'Phantom', 2015, 2, '12Feb2015_Zipser_Pilots_Phantom', 'mb_bold_mb6_20mm_AP_PSN_', [6]);
    my_dicom_to_nii( 'Phantom', 2015, 2, '12Feb2015_Zipser_Pilots_Phantom', 'gre_field_mapping_', [9 10]);
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if 0 %%%%%% 9 Feb 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
    my_dicom_to_nii( 'HVO', 2015, 2, '9Feb2015_Zipser_Pilots_HVO', 'mb_bold_mb6_20mm_AP_PSN_', [6 8 11 13]);
    my_dicom_to_nii( 'HVO', 2015, 2, '9Feb2015_Zipser_Pilots_HVO', 'gre_field_mapping_', [9]);
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


if 0 %%%%%% 7 Feb 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
    %my_dicom_to_nii( 'HVO', 2015, 2, '6Feb2015_Zipser_Pilots_HVO', 'mb_bold_mb6_15mm_PSN_', [4 6 8 10]);
    %my_dicom_to_nii( 'CW', 2015, 2, '7Feb2015_Zipser_Pilots_CW', 'mb_bold_mb6_20mm_AP_PSN_', [4 6 8 10 12 14]);
    %my_dicom_to_nii( 'Phantom', 2015, 2, '7Feb2015_Zipser_Pilots', 'mb_bold_mb6_20mm_AP_PSN_', [4 10 12 14 16]);
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if 0 %%%%%% 5 Feb 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
    %my_dicom_to_nii( 'Phantom', 2015, 1, '26Jan2015_MB_test_Zipser_Pilot_13Nov2014', 'mb_bold_mb4_15mm_AP_PSN_', [12]);
    %my_dicom_to_nii( 'Phantom', 2015, 1, '29Jan2015_MB_test_Zipser_Pilot_13Nov2014', 'mb_bold_mb1_15mm_AP_PSN_', [6]);
end %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if 0 %%%%%% 5 Feb 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
%%%%%%%%%%%%%%%%%%%%%%%%%%%% input %%%%%%%%%%%%%%%%%%%%%%%%%%%
    subject = 'Phantom';
    year = 2015;
    month = 1;
    session = '29Jan2015_MB_test_Zipser_Pilot_13Nov2014';
    protocol_name = 'mb_bold_mb6_15mm_Partial_PSN_';
    runs = [18 20];
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    fifty_path = '~/Desktop/Data/osx/50';
    session_path = d2s({'~/Desktop/Data/subjects/' subject '/' year '/' month '/' session});
    dcm_base_path = d2s({session_path '/dcm'});
    nii_path = d2s({session_path '/nii'});
    h=waitbar(0,'processing'); movegui(h,'southeast');
    for i = 1:length(runs)
        waitbar(i/length(runs));
        tic
        dcm_path = d2s({dcm_base_path '/' protocol_name runs(i) });
        system_str1 = d2s({ fifty_path ' -b ~/.dcm2niigui/dcm2niigui.ini ' dcm_path});
        fps(system_str1);
        system(system_str1);
        system_str2 = d2s({'mv ' dcm_path '/*.nii.gz ' nii_path});
        fps(system_str2);
        system(system_str2);
        toc
    end
    close(h);    
end


if 0 %%%%%% 5 Feb 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
    fifty_path = '~/Desktop/Data/osx/50';
    dcm_base_path = '~/Desktop/Data/subjects/Phantom/2015/1/26Jan2015_MB_test_Zipser_Pilot_13Nov2014/dcm';
    dcm_protocol_name = 'mb_bold_mb6_15mm_AP_PSN_';
    PSN_dcm_runs = [4];%[4 6 8];
    nii_path = '~/Desktop/Data/subjects/Phantom/2015/1/26Jan2015_MB_test_Zipser_Pilot_13Nov2014/nii';
 
    h=waitbar(0,'processing'); movegui(h,'southeast');
    for i = 1:length(PSN_dcm_runs)
        waitbar(i/length(PSN_dcm_runs));
        tic
        dcm_path = d2s({dcm_base_path '/' dcm_protocol_name PSN_dcm_runs(i) });

        system_str1 = d2s({ fifty_path ' -b ~/.dcm2niigui/dcm2niigui.ini ' dcm_path});
        fps(system_str1);
        system(system_str1);
        system_str2 = d2s({'mv ' dcm_path '/*.nii.gz ' nii_path});
        fps(system_str2);
        system(system_str2);
        toc
    end
    close(h);    
end


if 0 %%%%%% 3 Feb 2015 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;

    fifty_path = '~/Desktop/Data/osx/50';
    dcm_base_path = '~/Desktop/Data/subjects/HVO/2015/2/3Feb2015_Zipser_Pilots_HVO/dcm';
    dcm_protocol_name = 'mb_bold_mb6_15mm_PSN_';%'mb_bold_mb6_15mm_Partial_PSN_';
    PSN_dcm_runs = [10];%[4 6 8];
    nii_path = '~/Desktop/Data/subjects/HVO/2015/2/3Feb2015_Zipser_Pilots_HVO/nii';
    
    h=waitbar(0,'processing'); movegui(h,'southeast');
    for i = 1:length(PSN_dcm_runs)
        waitbar(i/length(PSN_dcm_runs));
        tic
        dcm_path = d2s({dcm_base_path '/' dcm_protocol_name PSN_dcm_runs(i) });

        system_str1 = d2s({ fifty_path ' -b ~/.dcm2niigui/dcm2niigui.ini ' dcm_path});
        fps(system_str1);
        system(system_str1);
        system_str2 = d2s({'mv ' dcm_path '/*.nii.gz ' nii_path});
        fps(system_str2);
        system(system_str2);

        toc
    end
    close(h);
end

if 0 %%%%%%30 Jan 2015%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
    fifty_path = '~/Desktop/Data/osx/50'
    PSN_dcm_runs = [14];%[8 10 12];%[6 8 10 12]
    
    h=waitbar(0,'processing'); movegui(h,'southeast');
    for i = 1:length(PSN_dcm_runs)
        waitbar(i/length(PSN_dcm_runs));
        tic
        dcm_path = d2s({'~/Desktop/Data/subjects/HVO/2015/1/30Jan2015_Zipser_Pilots_HVO/dcm/mb_bold_mb6_15mm_PSN_' PSN_dcm_runs(i) });
        nii_path = '~/Desktop/Data/subjects/HVO/2015/1/30Jan2015_Zipser_Pilots_HVO/nii';
        system(d2s({ fifty_path ' -b ~/.dcm2niigui/dcm2niigui.ini ' dcm_path}));
        d2s({'mv ' dcm_path '/*.nii.gz ' nii_path})
        toc
    end
    close(h);
end

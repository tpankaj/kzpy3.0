clc
clear folders_to_alias;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%% SPECIFIY WHAT TO DO %%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

folders_to_alias = {...
    {'~/Google_Drive','~/Desktop/Google_Drive'},...
    {'~/Google_Drive/analysis.matlab4/2015/3','~/Desktop/_analysis.matlab4.2015.3'},...
    {'~/Google_Drive/CURRENT BIC 3T fMRI experiments','~/Desktop/_CURRENT BIC 3T fMRI experiments'},...
    {'~/Google_Drive/21Jan2015 LITERATURE reorganized','~/Desktop/_21Jan2015 LITERATURE reorganized'},...
    {'~/Google_Drive/21Oct2014 interesting photos from online','~/Desktop/_interesting photos from online'},...
    {'~/Google_Drive/2015/1/bookmarks.rtf','~/Desktop/_Bookmarks'},...
    {'~/Google_Drive/Data','~/Desktop/_Data'}
    };

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%% END SPECIFIY WHAT TO DO %%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%% DO IT %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
for i = 1:length(folders_to_alias)
    if length(dir(folders_to_alias{i}{2})) == 0
        sys_str = ['ln -s ' unix_str(folders_to_alias{i}{1}) ' ' unix_str(folders_to_alias{i}{2})];
        fps(sys_str);
        system(sys_str);
    else
        fps([folders_to_alias{i}{2} ' already exists']);
    end
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


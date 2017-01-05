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


if 0 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 1;
'here'
    G.temp.d = dir('*.pdf');
    G.temp.current_dir = strrep((pwd),[G.home '/Google Drive/'],'');
    fprintf('%s\n', G.temp.current_dir);
    for i = 1:length(G.temp.d)
        str = d2s({i ') ' G.temp.d(i).name });% '    ' d(i).date });
        fprintf( '%s\n', str );
    end
end

if 1 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
CELL_NUM = 10;
    G.literature.md = {};
    k=G.literature.marked.keys();
    for n=1:length(k)
        G.literature.md{n} = k{n};
        fps(d2s({n ')  ' G.literature.md{n}}));
%        G.literature.marked(k{n})
%         cd ~/Google' Drive'/; cd(G.literature.marked(k{n}).dir);
%         open(k{n})
%         pwd
    end
    

end

%i = 36;system(d2s({'open ' unix_str(d(i).name)}));


% paper_paths = {...
% {'~/Google Drive/21Jan2015 LITERATURE reorganized/dated_downloads/2014/7/1July2014 fMRI texture V1 paper downloads/2003 Differential Contribution of Early Visual Areas to the Perceptual Process of Contour Processing.pdf'},...
% {'~/Google Drive/21Jan2015 LITERATURE reorganized/dated_downloads/2014/7/1July2014 fMRI texture V1 paper downloads/2012 Figure-Ground Representation and Its Decay in Primary Visual Cortex.pdf'},...
% {'~/Google Drive/21Jan2015 LITERATURE reorganized/dated_downloads/2014/7/2July2014 paper downloads/2014 The Lateral Occipital Complex Subserves the Perceptual Persistence of Motion-defined Groupings.pdf'},...
% {'~/Google Drive/21Jan2015 LITERATURE reorganized/dated_downloads/2014/7/2July2014 paper downloads/2013 Distinct Roles of the Cortical Layers of Area V1 in Figure-Ground Segregation.pdf'},...
% {'~/Google Drive/21Jan2015 LITERATURE reorganized/dated_downloads/2014/7/2July2014 paper downloads/2013 Decoding face categories in diagnostic subregions of primary visual cortex.pdf'},...
% {'~/Google Drive/21Jan2015 LITERATURE reorganized/dated_downloads/2014/7/2July2014 paper downloads/2013 Attention modulates spatial priority maps in the human occipital, parietal and frontal cortices.pdf'},...
% {'~/Google Drive/21Jan2015 LITERATURE reorganized/dated_downloads/2014/7/2July2014 paper downloads/2011 Object-based attention to one of two superimposed surfaces alters responses in human early visual cortex.pdf'},...
% {'~/Google Drive/21Jan2015 LITERATURE reorganized/dated_downloads/2014/7/2July2014 paper downloads/2011 Object-based attention to one of two superimposed surfaces alters responses in human early visual cortex.pdf'},...
% {'~/Google Drive/21Jan2015 LITERATURE reorganized/dated_downloads/2014/7/2July2014 paper downloads/2010 A backward progression of attentional effects in the ventral stream.pdf'},...
% {'~/Google Drive/21Jan2015 LITERATURE reorganized/dated_downloads/2014/7/2July2014 paper downloads/2009 The Topography of Visuospatial Attention as Revealed by a Novel Visual Field Mapping Technique.pdf'},...
% {'~/Google Drive/21Jan2015 LITERATURE reorganized/dated_downloads/2014/7/2July2014 paper downloads/2008 Occipital network for figure-ground organization.pdf'},...
% {'~/Google Drive/21Jan2015 LITERATURE reorganized/dated_downloads/2014/7/2July2014 paper downloads/2008 Feedback of visual object information to foveal retinotopic cortex.pdf'},...
% {'~/Google Drive/21Jan2015 LITERATURE reorganized/dated_downloads/2014/7/2July2014 paper downloads/2007 Figure-ground mechanisms provide structure for selective attention.pdf'},...
% {'~/Google Drive/21Jan2015 LITERATURE reorganized/dated_downloads/2014/7/8July2014 paper downloads/2014 Figure-Ground Processing during Fixational Saccades in V1, Indication for Higher-Order Stability.pdf'},...
% {'~/Google Drive/21Jan2015 LITERATURE reorganized/dated_downloads/2014/7/8July2014 paper downloads/2013 non-geniculate input to V1.pdf'},...
% {'~/Google Drive/21Jan2015 LITERATURE reorganized/dated_downloads/2014/7/8July2014 paper downloads/2012 V1 representations in natural and reduced visual contexts.pdf'},...
% {'~/Google Drive/21Jan2015 LITERATURE reorganized/dated_downloads/2014/7/8July2014 paper downloads/2009 Spatially Global Representations in Human Primary Visual Cortex during Working Memory Maintenance.pdf'},...
% {'~/Google Drive/21Jan2015 LITERATURE reorganized/dated_downloads/2014/7/8July2014 paper downloads/2009 Decoding reveals the contents of visual working memory in early visual areas.pdf'},...
% {'~/Google Drive/21Jan2015 LITERATURE reorganized/dated_downloads/2014/7/8July2014 paper downloads/2004 Long-distance feedback projections to area V1, Implications for multisensory integration, spatial awareness, and visual consciousness.pdf'},...
% {'~/Google Drive/21Jan2015 LITERATURE reorganized/dated_downloads/2014/7/13July2013 paper downloads/2014 Decoding individual natural scene representations during perception and imagery.pdf'},...
% {'~/Google Drive/21Jan2015 LITERATURE reorganized/dated_downloads/2014/7/13July2013 paper downloads/2012 Neural responses to visual scenes reveals inconsistencies between fMRI adaptation and multivoxel pattern analysis.pdf'},...
% };
% for i = 1:length(paper_paths)
%     sys_str =['open ' unix_str(paper_paths{i}{1})];
%     system(sys_str);
% end
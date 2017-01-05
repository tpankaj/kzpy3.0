selected = [14 18   38   42  58 72 88 98];

for i = 1:length(selected)
    img = selected(i);
    mi(S1_vri_dataset.V1.Val(img).average.z_img,1,[1,3,2],'V1 (S1)');
    mi(S1_vri_dataset.V2.Val(img).average.z_img,1,[1,3,3],'V2 (S1)');
    mi(G.stimVal512_uint8(img,:,:),1,[1,3,1],d2s({img}))
    pause
end
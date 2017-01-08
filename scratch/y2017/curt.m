% --------------------------------------------------------------------
% UDP packet receiver for Eagle / Ultra Radar sensor
% by Curt Hillier, NXP Semiconductor
% December 19, 2016
% --------------------------------------------------------------------
% The following code is used to import data directly from the UDP port
% without using Wireshark interface.  Packets are received using the
% UDPReceiver on UDP port 12345.
% Received packets are either stored to a file for later processing or
% displayed in near real time.
% For the display option, both the time domain and the frequency domain
% plots are shown.
 
% Set outputChoice:  1 = output to file, 2 = output to display
%outputChoice = 1; % output to file
outputChoice = 2; % output to display
% initialize arrays
Rx1Array = zeros(1024);
Rx2Array = zeros(1024);
Rx3Array = zeros(1024);
Rx4Array = zeros(1024);
dataReceived1 = zeros(1027); % setup array for receiving 1st packet
dataReceived2 = zeros(1027); % setup array for receiving 2nd packet
% setup the udp receiver
hudpr3 = dsp.UDPReceiver('LocalIPPort',12345, 'MaximumMessageLength', 1069, 'ReceiveBufferSize', 10270);
setup(hudpr3);
% setup filename for output to file or setup figure for display
if outputChoice == 1   % output to file
  filename = 'C:\Users\b31139\Projects2\bdd_radar\test.txt';
  fid = fopen(filename, 'w');
end
if outputChoice == 2   % output to display
   fig = figure;
end
t = cputime;
emptyCount = 0;
for j = 1:10000
  % read 2 packets from the UDP object
  % first packet contains ADC channels 1 and 2
  % second packet contains ADC channels 3 and 4
  % packet data length is 1027
  dataReceived1 = hudpr3.step();
  dataReceived2 = hudpr3.step();
  % Matlab appears to read too fast for the packet arrivals,
  % some packets are empty. The following checks for empty
  % packets before writing data to file or displaying received packet
  % contents.
  if isempty(dataReceived1)
      emptyCount = emptyCount+1;
  else
      if outputChoice == 1    % output to file
          fprintf(fid, '%d', dataReceived1);
          fprintf(fid, '\n');
      end
      if outputChoice == 2    % output to display
          adcData = dataReceived1(4:1027);
          for i = 0:255
             bytepack=int16(adcData(2*i+1));
             bytepack=bitshift(bytepack,8);
             % Put them together (here, 'y' is placed in lower 8 bits)
             z(i+1)=bitor(bytepack,int16(adcData(2*i+2)));
          end
          plot(z);
          ax1 = subplot(2,1,1);
          plot(ax1,z);
          ylim([-10000 10000]); 
          
          % ==== do the FFT ====
          % Calculate FFT using MATLAB function
          Fs = 10000000;   % 10 MHz sampling rate
          nPts=256;
          SF=fft(double(z),nPts);
          %tempSF = abs(SF(1:nPts/2)/(nPts/2));
          magSF=20*log10(abs(SF(1:nPts/2)/(nPts/2)));  % calculate magnitude. MB: divide by nPts/2 since FFT has gain.
          f = (0:Fs/(2*(length(magSF)-1)):(Fs/2));     % get the frequency bins
          magSF_max=max(magSF);                        % find max magnitude
          magSF=magSF-magSF_max;                       % adjust down by max magnitude
          subplot(2,1,2)                               % plot of 4 rows by 2 columns.  subplot 4
          plot(f,magSF);grid;                          % plot the FFT results
          ylim([-80 0]);                               % set the y axis limits
          xlabel('Frequency (Hz)');ylabel('Magnitude');title('Signal spectrum');
          % ====================
      end
         
  end
 
  %if isempty(dataReceived2)
  %    emptyCount = emptyCount+1;
  %else
  %   fprintf(fid, '%d', dataReceived2);
  %   fprintf(fid, '\n'); 
  %end
 
  % rate adjust, packets arrive every 1.5 ms
  pause(0.0001)
end
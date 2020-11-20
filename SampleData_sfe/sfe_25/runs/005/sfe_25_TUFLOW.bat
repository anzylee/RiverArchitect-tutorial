Set TF_Exe="C:\Program Files\Tuflow_w64\TUFLOW_iSP_w64.exe"
Set RUN=start "TUFLOW" %TF_Exe%

%RUN% -b "F:\tuflow-wf_python3\output_folder\sfe_25_tuflow\runs\\005\sfe_25.tcf" 
pause
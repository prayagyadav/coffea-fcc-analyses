condor_q pryadav -autoformat ClusterId ProcId | awk '{print $1"."$2}' | while read jobid; do
    echo "Resubmitting ..."
    echo "----> JobID: ${jobid}"
    sequencenumber=$(ls log-*.${jobid} 2>/dev/null | sed -E 's/log-([^.]+)\..*/\1/')
    echo "----> Sequence Number: ${sequencenumber}"
    condor_submit submit_${sequencenumber}.sh
    sleep 2.5
    condor_rm ${jobid}
    sleep 2.5
    echo "----> Removed held job: ${jobid}"
    
done


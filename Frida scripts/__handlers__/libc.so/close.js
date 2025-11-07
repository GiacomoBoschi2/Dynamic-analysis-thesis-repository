defineHandler({
  onEnter(log, args, state) {
    log(`close(fd=${args[0]})`);
    try {
      try {
        Java.perform(function () {
          try {
            var Thread = Java.use('java.lang.Thread');
            var cur = Thread.currentThread();
            var st = cur.getStackTrace();
            var javaFrames = [];
            for (var i = 0; i < st.length; i++) {
              try { javaFrames.push(st[i].toString()); } catch (ee) {}
            }
            if (javaFrames.length > 0) {
              log("JAVA STACK")
              for(let i = 0;i<javaFrames.length;i++){
                    log((i+1)+") "+javaFrames[i])
              }
              log("\n");
            }
          } catch (je) {
            
          }
        });
      } catch (e) {
        
      }
    } catch (err) {
      log('[connect.enter] handler error: ' + err);
    }
  },

  onLeave(log, retval, state) {
  }
});

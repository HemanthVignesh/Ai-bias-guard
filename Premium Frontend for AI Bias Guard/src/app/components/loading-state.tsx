import { motion } from "motion/react";
import { Brain, Zap } from "lucide-react";

export function LoadingState() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="max-w-3xl mx-auto"
    >
      <div className="relative group">
        <div className="absolute -inset-0.5 bg-gradient-to-r from-purple-600 via-blue-600 to-purple-600 rounded-2xl opacity-50 blur animate-pulse" />
        
        <div className="relative bg-card/80 backdrop-blur-xl border border-purple-500/20 rounded-2xl p-8">
          <div className="flex flex-col items-center justify-center gap-6">
            {/* Animated icon */}
            <div className="relative">
              <motion.div
                className="absolute inset-0 rounded-full bg-purple-500/20"
                animate={{
                  scale: [1, 1.5, 1],
                  opacity: [0.5, 0, 0.5],
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  ease: "easeInOut",
                }}
              />
              <div className="relative p-4 rounded-full bg-purple-500/20 border border-purple-500/30">
                <motion.div
                  animate={{
                    rotate: [0, 360],
                  }}
                  transition={{
                    duration: 3,
                    repeat: Infinity,
                    ease: "linear",
                  }}
                >
                  <Brain className="w-12 h-12 text-purple-400" />
                </motion.div>
              </div>
            </div>

            {/* Loading text */}
            <div className="text-center space-y-2">
              <h3 className="text-xl font-semibold text-foreground">
                Analyzing Your Text
              </h3>
              <p className="text-sm text-muted-foreground">
                Running bias detection models...
              </p>
            </div>

            {/* Progress steps */}
            <div className="w-full max-w-md space-y-3">
              {[
                { label: "Tokenizing text", delay: 0 },
                { label: "Running BART analysis", delay: 0.3 },
                { label: "Generating mitigation", delay: 0.6 },
              ].map((step, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: step.delay }}
                  className="flex items-center gap-3"
                >
                  <motion.div
                    className="w-2 h-2 rounded-full bg-purple-400"
                    animate={{
                      scale: [1, 1.5, 1],
                      opacity: [1, 0.5, 1],
                    }}
                    transition={{
                      duration: 1.5,
                      delay: step.delay,
                      repeat: Infinity,
                      ease: "easeInOut",
                    }}
                  />
                  <span className="text-sm text-muted-foreground">{step.label}</span>
                  <motion.div
                    className="ml-auto"
                    animate={{ rotate: 360 }}
                    transition={{
                      duration: 2,
                      repeat: Infinity,
                      ease: "linear",
                    }}
                  >
                    <Zap className="w-4 h-4 text-blue-400" />
                  </motion.div>
                </motion.div>
              ))}
            </div>

            {/* Progress bar */}
            <div className="w-full max-w-md">
              <div className="h-2 bg-purple-500/10 rounded-full overflow-hidden">
                <motion.div
                  className="h-full bg-gradient-to-r from-purple-500 to-blue-500"
                  initial={{ width: "0%" }}
                  animate={{ width: "100%" }}
                  transition={{
                    duration: 2,
                    ease: "easeInOut",
                    repeat: Infinity,
                  }}
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

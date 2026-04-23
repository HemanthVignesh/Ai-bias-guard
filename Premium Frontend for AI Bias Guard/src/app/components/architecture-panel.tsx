import { motion, AnimatePresence } from "motion/react";
import { X, Server, Shield, Zap, Lock } from "lucide-react";

interface ArchitecturePanelProps {
  isOpen: boolean;
  onClose: () => void;
}

export function ArchitecturePanel({ isOpen, onClose }: ArchitecturePanelProps) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40"
          />

          {/* Panel */}
          <motion.div
            initial={{ x: "100%" }}
            animate={{ x: 0 }}
            exit={{ x: "100%" }}
            transition={{ type: "spring", damping: 25, stiffness: 200 }}
            className="fixed right-0 top-0 bottom-0 w-full md:w-[500px] bg-card/95 backdrop-blur-xl border-l border-purple-500/20 shadow-2xl z-50 overflow-y-auto"
          >
            <div className="p-8">
              {/* Header */}
              <div className="flex items-start justify-between mb-8">
                <div>
                  <h2 className="text-3xl font-bold bg-gradient-to-r from-purple-400 to-blue-500 bg-clip-text text-transparent mb-2">
                    Architecture
                  </h2>
                  <p className="text-muted-foreground">Fully Local AI System</p>
                </div>
                <button
                  onClick={onClose}
                  className="p-2 rounded-lg hover:bg-purple-500/20 transition-colors"
                >
                  <X className="w-6 h-6 text-muted-foreground" />
                </button>
              </div>

              {/* Features */}
              <div className="space-y-6 mb-8">
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 }}
                  className="relative group"
                >
                  <div className="absolute -inset-0.5 bg-gradient-to-r from-purple-600 to-blue-600 rounded-xl opacity-30 group-hover:opacity-50 blur transition duration-300" />
                  <div className="relative bg-card border border-purple-500/20 rounded-xl p-6">
                    <div className="flex items-start gap-4">
                      <div className="p-3 rounded-lg bg-purple-500/20">
                        <Lock className="w-6 h-6 text-purple-400" />
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold text-purple-300 mb-2">
                          100% Local Processing
                        </h3>
                        <p className="text-sm text-muted-foreground leading-relaxed">
                          All analysis happens on your device. No data is sent to external servers,
                          ensuring complete privacy and security.
                        </p>
                      </div>
                    </div>
                  </div>
                </motion.div>

                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 }}
                  className="relative group"
                >
                  <div className="absolute -inset-0.5 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl opacity-30 group-hover:opacity-50 blur transition duration-300" />
                  <div className="relative bg-card border border-blue-500/20 rounded-xl p-6">
                    <div className="flex items-start gap-4">
                      <div className="p-3 rounded-lg bg-blue-500/20">
                        <Zap className="w-6 h-6 text-blue-400" />
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold text-blue-300 mb-2">
                          No API Keys Required
                        </h3>
                        <p className="text-sm text-muted-foreground leading-relaxed">
                          Run the system without any external API dependencies. Perfect for
                          sensitive data and offline environments.
                        </p>
                      </div>
                    </div>
                  </div>
                </motion.div>
              </div>

              {/* Models */}
              <div className="space-y-4">
                <h3 className="text-xl font-semibold text-foreground mb-4 flex items-center gap-2">
                  <Server className="w-5 h-5 text-purple-400" />
                  AI Models
                </h3>

                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.3 }}
                  className="relative group"
                >
                  <div className="absolute -inset-0.5 bg-gradient-to-r from-emerald-500 to-green-500 rounded-xl opacity-20 blur" />
                  <div className="relative bg-card/50 border border-emerald-500/20 rounded-xl p-5">
                    <div className="flex items-center gap-3 mb-3">
                      <div className="p-2 rounded-lg bg-emerald-500/20">
                        <Shield className="w-5 h-5 text-emerald-400" />
                      </div>
                      <div>
                        <h4 className="font-semibold text-emerald-300">BART Model</h4>
                        <p className="text-xs text-muted-foreground">Bias Detection Engine</p>
                      </div>
                    </div>
                    <p className="text-sm text-muted-foreground leading-relaxed">
                      A fine-tuned BART (Bidirectional and Auto-Regressive Transformers) model
                      specialized in identifying potential bias patterns across multiple dimensions
                      including gender, race, age, and cultural references.
                    </p>
                  </div>
                </motion.div>

                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.4 }}
                  className="relative group"
                >
                  <div className="absolute -inset-0.5 bg-gradient-to-r from-blue-500 to-purple-500 rounded-xl opacity-20 blur" />
                  <div className="relative bg-card/50 border border-blue-500/20 rounded-xl p-5">
                    <div className="flex items-center gap-3 mb-3">
                      <div className="p-2 rounded-lg bg-blue-500/20">
                        <Zap className="w-5 h-5 text-blue-400" />
                      </div>
                      <div>
                        <h4 className="font-semibold text-blue-300">T5 Model</h4>
                        <p className="text-xs text-muted-foreground">Bias Mitigation Engine</p>
                      </div>
                    </div>
                    <p className="text-sm text-muted-foreground leading-relaxed">
                      T5 (Text-to-Text Transfer Transformer) generates neutral alternatives by
                      rewriting biased content while preserving the original meaning and context,
                      ensuring fair and inclusive language.
                    </p>
                  </div>
                </motion.div>
              </div>

              {/* Pipeline Info */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
                className="mt-8 p-6 rounded-xl bg-purple-500/10 border border-purple-500/20"
              >
                <h4 className="font-semibold text-purple-300 mb-3">Processing Pipeline</h4>
                <ol className="space-y-3 text-sm text-muted-foreground">
                  <li className="flex gap-3">
                    <span className="flex-shrink-0 w-6 h-6 rounded-full bg-purple-500/20 flex items-center justify-center text-purple-400 font-semibold">
                      1
                    </span>
                    <span>Text input is tokenized and preprocessed</span>
                  </li>
                  <li className="flex gap-3">
                    <span className="flex-shrink-0 w-6 h-6 rounded-full bg-purple-500/20 flex items-center justify-center text-purple-400 font-semibold">
                      2
                    </span>
                    <span>BART model analyzes for bias patterns</span>
                  </li>
                  <li className="flex gap-3">
                    <span className="flex-shrink-0 w-6 h-6 rounded-full bg-purple-500/20 flex items-center justify-center text-purple-400 font-semibold">
                      3
                    </span>
                    <span>Confidence score and gaps are calculated</span>
                  </li>
                  <li className="flex gap-3">
                    <span className="flex-shrink-0 w-6 h-6 rounded-full bg-purple-500/20 flex items-center justify-center text-purple-400 font-semibold">
                      4
                    </span>
                    <span>T5 model generates mitigated version</span>
                  </li>
                  <li className="flex gap-3">
                    <span className="flex-shrink-0 w-6 h-6 rounded-full bg-purple-500/20 flex items-center justify-center text-purple-400 font-semibold">
                      5
                    </span>
                    <span>Results are presented with reasoning</span>
                  </li>
                </ol>
              </motion.div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}

import { motion } from "motion/react";
import { AlertTriangle, CheckCircle, Brain, Lightbulb } from "lucide-react";
import { BiasGauge } from "./bias-gauge";

interface ResultsDashboardProps {
  biasDetected: boolean;
  confidence: number;
  mitigatedText: string;
  detectedGaps: string[];
  reasoning: string;
  originalText: string;
}

export function ResultsDashboard({
  biasDetected,
  confidence,
  mitigatedText,
  detectedGaps,
  reasoning,
  originalText,
}: ResultsDashboardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="max-w-6xl mx-auto space-y-6"
    >
      {/* Status and Gauge Row */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Status Card */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2, duration: 0.5 }}
          className="relative group"
        >
          <div
            className={`absolute -inset-0.5 rounded-2xl opacity-50 blur transition duration-300 ${
              biasDetected
                ? "bg-gradient-to-r from-orange-500 to-red-500"
                : "bg-gradient-to-r from-emerald-500 to-green-500"
            }`}
          />
          <div className="relative bg-card/80 backdrop-blur-xl border border-purple-500/20 rounded-2xl p-8">
            <div className="flex items-start gap-4">
              {biasDetected ? (
                <div className="p-3 rounded-xl bg-orange-500/20 border border-orange-500/30">
                  <AlertTriangle className="w-8 h-8 text-orange-400" />
                </div>
              ) : (
                <div className="p-3 rounded-xl bg-emerald-500/20 border border-emerald-500/30">
                  <CheckCircle className="w-8 h-8 text-emerald-400" />
                </div>
              )}
              <div className="flex-1">
                <h3
                  className={`text-2xl font-bold mb-2 ${
                    biasDetected ? "text-orange-400" : "text-emerald-400"
                  }`}
                >
                  {biasDetected ? "⚠️ Bias Detected" : "✅ Looks Neutral"}
                </h3>
                <p className="text-muted-foreground">
                  {biasDetected
                    ? "Potential bias patterns were identified in the text."
                    : "No significant bias patterns were detected."}
                </p>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Gauge Card */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3, duration: 0.5 }}
          className="relative group"
        >
          <div className="absolute -inset-0.5 bg-gradient-to-r from-purple-600 via-blue-600 to-purple-600 rounded-2xl opacity-30 blur" />
          <div className="relative bg-card/80 backdrop-blur-xl border border-purple-500/20 rounded-2xl p-8 flex items-center justify-center">
            <BiasGauge confidence={confidence} biasDetected={biasDetected} />
          </div>
        </motion.div>
      </div>

      {/* Original Text Card */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4, duration: 0.5 }}
        className="relative group"
      >
        <div className="absolute -inset-0.5 bg-gradient-to-r from-purple-600/30 to-blue-600/30 rounded-2xl opacity-50 blur" />
        <div className="relative bg-card/80 backdrop-blur-xl border border-purple-500/20 rounded-2xl p-6">
          <div className="flex items-center gap-2 mb-4">
            <div className="p-2 rounded-lg bg-purple-500/20">
              <Brain className="w-5 h-5 text-purple-400" />
            </div>
            <h3 className="text-xl font-semibold text-purple-300">Original Text</h3>
          </div>
          <p className="text-foreground/90 leading-relaxed">{originalText}</p>
        </div>
      </motion.div>

      {/* Mitigated Result Card */}
      {mitigatedText && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.5 }}
          className="relative group"
        >
          <div className="absolute -inset-0.5 bg-gradient-to-r from-emerald-500 to-green-500 rounded-2xl opacity-40 blur" />
          <div className="relative bg-card/80 backdrop-blur-xl border border-emerald-500/30 rounded-2xl p-6">
            <div className="flex items-center gap-2 mb-4">
              <div className="p-2 rounded-lg bg-emerald-500/20">
                <CheckCircle className="w-5 h-5 text-emerald-400" />
              </div>
              <h3 className="text-xl font-semibold text-emerald-300">Mitigated Result</h3>
            </div>
            <p className="text-foreground/90 leading-relaxed">{mitigatedText}</p>
          </div>
        </motion.div>
      )}

      {/* Detected Gaps */}
      {detectedGaps.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6, duration: 0.5 }}
          className="relative group"
        >
          <div className="absolute -inset-0.5 bg-gradient-to-r from-orange-500 to-red-500 rounded-2xl opacity-30 blur" />
          <div className="relative bg-card/80 backdrop-blur-xl border border-orange-500/30 rounded-2xl p-6">
            <div className="flex items-center gap-2 mb-4">
              <div className="p-2 rounded-lg bg-orange-500/20">
                <AlertTriangle className="w-5 h-5 text-orange-400" />
              </div>
              <h3 className="text-xl font-semibold text-orange-300">Detected Gaps</h3>
            </div>
            <ul className="space-y-2">
              {detectedGaps.map((gap, index) => (
                <motion.li
                  key={index}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.7 + index * 0.1 }}
                  className="flex items-start gap-2 text-foreground/90"
                >
                  <span className="text-orange-400 mt-1">•</span>
                  <span>{gap}</span>
                </motion.li>
              ))}
            </ul>
          </div>
        </motion.div>
      )}

      {/* AI Reasoning */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.7, duration: 0.5 }}
        className="relative group"
      >
        <div className="absolute -inset-0.5 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl opacity-30 blur" />
        <div className="relative bg-card/80 backdrop-blur-xl border border-blue-500/30 rounded-2xl p-6">
          <div className="flex items-center gap-2 mb-4">
            <div className="p-2 rounded-lg bg-blue-500/20">
              <Lightbulb className="w-5 h-5 text-blue-400" />
            </div>
            <h3 className="text-xl font-semibold text-blue-300">AI Reasoning</h3>
          </div>
          <p className="text-foreground/90 leading-relaxed">{reasoning}</p>
        </div>
      </motion.div>
    </motion.div>
  );
}

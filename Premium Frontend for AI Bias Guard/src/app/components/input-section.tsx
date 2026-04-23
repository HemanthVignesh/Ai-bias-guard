import { motion } from "motion/react";
import { Sparkles, Loader2, Zap } from "lucide-react";
import { useState } from "react";

interface InputSectionProps {
  onAnalyze: (text: string) => void;
  isLoading: boolean;
}

const EXAMPLE_TEXTS = [
  "The chairman will meet with the guys from engineering to discuss the new features.",
  "She is a skilled engineer who works with the development team.",
  "The elderly man needs assistance with his computer setup.",
];

export function InputSection({ onAnalyze, isLoading }: InputSectionProps) {
  const [inputText, setInputText] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputText.trim() && !isLoading) {
      onAnalyze(inputText);
    }
  };

  const handleExampleClick = (example: string) => {
    setInputText(example);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3, duration: 0.6 }}
      className="max-w-3xl mx-auto mb-12"
    >
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Glass card container */}
        <div className="relative group">
          {/* Animated border glow */}
          <div className="absolute -inset-0.5 bg-gradient-to-r from-purple-600 via-blue-600 to-purple-600 rounded-2xl opacity-30 group-hover:opacity-50 blur transition duration-500 group-focus-within:opacity-60" />
          
          <div className="relative">
            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Enter text to analyze for potential bias..."
              className="w-full h-32 px-6 py-4 bg-card/80 backdrop-blur-xl border border-purple-500/20 rounded-2xl text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-purple-500/50 transition-all duration-300 resize-none"
              disabled={isLoading}
            />
          </div>
        </div>

        {/* Example texts */}
        <div className="flex flex-wrap gap-2">
          <span className="text-sm text-muted-foreground flex items-center gap-1">
            <Zap className="w-3 h-3" />
            Try examples:
          </span>
          {EXAMPLE_TEXTS.map((example, index) => (
            <motion.button
              key={index}
              type="button"
              onClick={() => handleExampleClick(example)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="text-xs px-3 py-1.5 rounded-lg bg-purple-500/10 border border-purple-500/20 text-purple-300 hover:bg-purple-500/20 hover:border-purple-500/40 transition-all duration-200"
              disabled={isLoading}
            >
              Example {index + 1}
            </motion.button>
          ))}
        </div>

        {/* Analyze button */}
        <motion.button
          type="submit"
          disabled={!inputText.trim() || isLoading}
          className="relative w-full group disabled:opacity-50 disabled:cursor-not-allowed"
          whileHover={{ scale: inputText.trim() && !isLoading ? 1.02 : 1 }}
          whileTap={{ scale: inputText.trim() && !isLoading ? 0.98 : 1 }}
        >
          {/* Animated gradient background */}
          <div className="absolute -inset-0.5 bg-gradient-to-r from-purple-600 via-blue-600 to-purple-600 rounded-xl opacity-75 group-hover:opacity-100 blur transition duration-300 group-disabled:opacity-50" />
          
          <div className="relative flex items-center justify-center gap-3 px-8 py-4 bg-gradient-to-r from-purple-600 to-blue-600 rounded-xl transition-all duration-300">
            {isLoading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span className="font-semibold text-white">Analyzing...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5 text-white" />
                <span className="font-semibold text-white">Analyze & Mitigate</span>
              </>
            )}
          </div>
        </motion.button>

        {/* Character counter */}
        {inputText && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-sm text-muted-foreground text-right"
          >
            {inputText.length} characters
          </motion.div>
        )}
      </form>
    </motion.div>
  );
}
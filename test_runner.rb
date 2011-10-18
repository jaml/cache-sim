LOOPS = [10, 20, 30, 50, 80, 100, 150, 200, 250, 300]

def gen_files block_size, word_size, cache_type, loop_size
  `python src/gen_tracefile.py #{block_size} #{word_size} #{cache_type} #{loop_size}`
end

def run_test block_size, word_size, type, loop_size
  gen_files block_size, word_size, type, loop_size
  unfused_output = `python src/trace.py unfused.trace`.chomp.split[2]
  fused_output = `python src/trace.py fused.trace`.chomp.split[2]
  puts "#{loop_size} | #{unfused_output} | #{fused_output}"
end

LOOPS.each do |i|
  run_test ARGV[0], ARGV[1], ARGV[2], i
end
